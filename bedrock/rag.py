import json
import boto3

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_aws import ChatBedrock
from langchain_aws import AmazonKnowledgeBasesRetriever

from typing import List, Dict
from pydantic import BaseModel

class Citation(BaseModel):
    page_content: str
    metadata: Dict

def extract_citations(context: List[Dict]) -> List[Citation]:
    return [Citation(page_content=doc.page_content, metadata=doc.metadata) for doc in context]

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

model_id = "anthropic.claude-3-haiku-20240307-v1:0"

model_kwargs =  { 
    "max_tokens": 2048,
    "temperature": 0.0,
    "stop_sequences": ["\n\nHuman"],
}

def lambda_handler(event, context):
    
    template = '''Answer the question based only on the following context:
    {context}
    
    Question: {question}'''
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Amazon Bedrock - KnowledgeBase Retriever 
    retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id="R1Y0IURZU1",
        retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 3}},
    )
    
    model = ChatBedrock(
        client=bedrock_runtime,
        model_id=model_id,
        model_kwargs=model_kwargs,
    )
    
    chain = (
        RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
        .assign(response = prompt | model | StrOutputParser())
        .pick(["response", "context"])
    )
    
    response = chain.invoke("What is attention?")
    
    print(response['response'])
    
    citations = extract_citations(response['context'])

    for citation in citations:
        print(f"Page Content: {citation.page_content}")
        print("Source:", citation.metadata['location']['s3Location']['uri'])
        print("Score:", citation.metadata['score'])
        print()
        
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }




