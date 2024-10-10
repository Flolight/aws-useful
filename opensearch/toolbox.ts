import {defaultProvider } from '@aws-sdk/credential-provider-node';
import { Client } from '@opensearch-project/opensearch';
import { AwsSigv4Signer } from '@opensearch-project/opensearch/aws';

const osClient = new Client({
    ...AwsSigv4Signer({
        region: process.env.AWS_REGION as string,
        service: 'aoss',
        getCredentials: () => {
            const credentialsProvider = defaultProvider();
            return credentialsProvider();
        },
    }),
    node: process.env.OS_COLLECTION_ENDPOINT
});


async function test(){

    var index_name = "books";
    try{
    
        var settings = {
            settings: {
            index: {
                number_of_shards: 4,
                number_of_replicas: 3,
            },
            },
        };

        var response = await osClient.indices.create({
            index: index_name,
            body: settings,
        });
    } catch (error) {
        console.log(error);
        if (error.meta && error.meta.body) {
            console.log(JSON.stringify(error.meta.body, null, 2));
        }
    }

    console.log("Creating index:");
    console.log(response.body);

    // Add a document to the index
    var document = {
        title: "The Outsider",
        author: "Stephen King",
        year: "2018",
        genre: "Crime fiction",
    };

    var id = "1";

    // var response = await osClient.index({
    //     // id: id,
    //     index: index_name,
    //     body: document,
    //     // refresh: true,
    // });

    // console.log("Adding document:");
    // console.log(response.body);

    // Search for the document
    var query = {
        query: {
        match: {
            title: {
            query: "The Outsider",
            },
        },
        },
    };

    var response = await osClient.search({
        index: index_name,
        body: query,
    });

    console.log("Search results:");
    console.log(JSON.stringify(response.body.hits, null, "  "));

    // Update a document
    var response = await osClient.update({
        index: index_name,
        id: response.body.hits.hits[0]._id,
        body: {
        doc: {
            genre: "Detective fiction",
            tv_adapted: true
        }
        },
        // refresh: true
    });

    // Search for the updated document
    var query = {
        query: {
        match: {
            title: {
            query: "The Outsider",
            },
        },
        },
    };

    var response = await osClient.search({
        index: index_name,
        body: query,
    });

    console.log("Search results:");
    console.log(JSON.stringify(response.body.hits, null, "  "));

    // Delete the document
    var response = await osClient.delete({
        index: index_name,
        id: response.body.hits.hits[0]._id,
    });

    console.log("Deleting document:");
    console.log(response.body);

    // Delete the index
    var response = await osClient.indices.delete({
        index: index_name,
    });

    console.log("Deleting index:");
    console.log(response.body);
}
