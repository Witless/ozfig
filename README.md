# ozfig

In this project we have retrieved a LLM model (llama 3.1 8b), fine-tuned it
using the Finetome dataset, evaluated it and deployed it in an online inference wrapper.

The resulting inference application holding the model receives the name of **ozfig**.  

## Fine tuning flow 

![flow_of_the_model_fine_tune_process](https://i.imgur.com/exovvO6.png)

## Evaluation flow

![flow_of_the_evaluation_process](https://i.imgur.com/eozvQQt.png)

### Used Evals

### Results of the model performance

| Evaluation method  | Obtained score     | Wanted values |
|--------------------|--------------------|---------------|
| Evals w/ BERTScore | 0.705              | Closer to 1   |
| Perplexity         | 5.7923 +/- 0.03449 | Closer to 0   |

## Inference upgrade 

The model has been wrapped in an online inference application. 

At every inference the model uses the following prompts: 

```json
            {"role": "system", "content": "You are a helpful and detailed assistant called OzFig"},
            {"role": "user", "content": prompt}
```

With **_prompt_** being supercharged with online web content thanks to DuckDuckGo API: 

```python
    ---
    url = (
    f"https://api.duckduckgo.com/"
    f"?q={quote(query)}&format=json&no_redirect=1&no_html=1"
    )
    --- 

    web_snippets =  await fetch_duckduckgo(query)
    combined_web_snippets = " ".join(web_snippets)

    prompt = (f"Reply and have a conversation with the user, this is their prompt: --Beginning of User Prompt-- \"{query}\" "
              f"--End of User Prompt--. These are the results from the web, use them to compose a more detailed answer: \"{combined_web_snippets}\"")
```


The application provides the GET endpoint /prompt/{query} to chat with the LLM

## Deployment

### HuggingFace

The model has been deployed to a HuggingFace space. It can be accessed from: https://huggingface.co/spaces/pablo-e/llama3.1-finetuned-playground

### Docker image

Additionally, a "modelless" docker image has been created and published in the docker.io registry.

This can be accessed and downloaded from: https://hub.docker.com/repository/docker/witless/ozfig-modelless/general

The image can be run having the Docker engine and using the following command
```shell
docker run -d -p 80:8080 ozfig:latest
```

Once the application starts it will begin to download the model from HuggingFace. This process can take several minutes depending on your internet connection. 

When the model is downloaded, you can access the inference endpoint at _localhost/prompt/{your prompt}_





