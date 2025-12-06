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

| Evaluation method  | Obtained score     | Desired values |
|--------------------|--------------------|---------------|
| Average BERTScore Precision | 0.8634 | Closer to 1   |
| Average BERTScore Recall    | 0.8676 | Closer to 1   |
| Average BERTScore F1        | 0.8653 | Closer to 1   |
| Perplexity         | 5.7923 +/- 0.03449 | Closer to 0   |


## Comparison of Reference Answer vs. Model Output

### Prompt
```
How does IR spectroscopy work, and what information can it provide about a compound?
```

### Reference Answer (mlabonne/FineTome-100k)
```
Infrared (IR) spectroscopy is a technique that uses infrared radiation to excite the molecules of a compound and generates an infrared spectrum of the energy absorbed by a molecule as a function of the frequency or wavelength of light.

Different types of bonds respond to the IR radiation differently. For example, triple and double bonds are shorter and stiffer than single bonds, and therefore will vibrate at higher frequencies. The types of atoms involved in the bonds are also relevant. For example, O-H bonds are stronger than C-H bonds, so O-H bonds vibrate at higher frequencies. IR spectroscopy therefore allows us to identify the various functional groups present in a compound.

It is worth noting that a dipole moment is required for a molecule to absorb IR radiation. In general, if a bond has a dipole moment, its stretching frequency causes an absorption in the IR spectrum. If a bond is symmetrically substituted and has zero dipole moment, its stretching vibration is weak or entirely absent in the spectrum (IR-active vs. IR-inactive vibrations). However, bonds with zero dipole moments sometimes produce weak absorptions because molecular collisions, rotations, and vibrations make them unsymmetrical part of the time.

In summary, IR spectroscopy is a powerful tool for identifying functional groups and studying the structure of organic compounds.
```
### Model Output
```
Infrared (IR) spectroscopy works by detecting the absorption of infrared light by a compound. Infrared light, which has wavelengths longer than visible light, can excite the vibrations of molecules, causing them to absorb specific frequencies of infrared radiation. The absorption of infrared light is specific to the chemical bonds and functional groups present in a molecule, allowing for the identification and characterization of compounds.

The information that IR spectroscopy can provide about a compound includes:

1. Molecular structure: IR spectroscopy can be used to identify functional groups and chemical bonds present in a molecule.
2. Chemical bonding: Positions and intensities of absorption bands provide information about bond types and strengths.
3. Identification: Unknown compounds can be identified by comparing their spectra with known spectra.
4. Quantification: Absorption band intensity can indicate concentration.
5. Polymer characterization: Functional groups and bonds in polymers can be analyzed.
6. Analytical chemistry: IR spectroscopy is widely used as an analytical tool.
```
BERTScore:
- Precision: 0.8775
- Recall: 0.8542
- F1: 0.8657

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





