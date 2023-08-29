# Lambda layers


## Python

- Find your docker image [here](https://gallery.ecr.aws/sam/build-python3.11) (choose your python version)

```sh
docker pull public.ecr.aws/sam/build-python3.10:1.84.0-20230517004040
docker run -it -v $(pwd):/var/task public.ecr.aws/sam/build-python3.10:1.84.0-20230517004040

pip install langchain openai tiktoken -t ./python
zip -r python.zip ./python
```
