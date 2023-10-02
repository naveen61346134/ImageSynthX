# ImageSynthX (Image Synthesizer And Generator)

## Description

**ImageSynthX**: Unleash the Power of AI Models for High-Resolution Image Synthesis and Enhancement. Transform your images with cutting-edge AI, including **`Real Esrgan`**, **`SDXL (Advanced Stable Diffusion)`**, and **`Cartoonify`**, to generate stunning, high-quality, and razor-sharp visuals.

## Table of Contents

- [ImageSynthX (Image Synthesizer And Generator)](#imagesynthx-image-synthesizer-and-generator)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [API Token](#api-token)
  - [Models](#models)
  - [Output](#output)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

To get started with this project, follow these steps:

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/naveen61346134/ImageSynthX.git
   ```

2. Navigate to the `Model Access` directory:

   ```
   cd REPLICATE-API-CALLS/Model\ Access
   ```

3. Install the required dependencies:

   ```
   run "installer.bat"
   ```

## Usage

To use this project, you need to obtain a **`Replicate API token`** (see [API Token](#api-token) section). Once you have the token, you can run the **`main.py`** script to access Replicate AI models. Here's how to use it:

```python
python main.py
```

Follow the prompts to select a model and provide any required inputs.

## API Token

To access Replicate AI models, you'll need an API token. Follow these steps to obtain a token:

1. Visit the [Replicate AI website](https://www.replicate.ai/).

2. Sign in or create an account if you haven't already.

3. Generate an API token in your account settings.

4. Save the generated token in a file named `token.txt` in the same directory as `main.py`.

## Models

This project currently supports the following Replicate AI models:

- **Real Esrgan**: Real Esrgan is an advanced AI model that `enhances image resolution` and `upscales content`, producing `sharper` and `more detailed visuals` through deep learning techniques.
- **SDXL**: SDXL is the evolutionary successor to the `Stable Diffusion AI model`, renowned for its ability to *transform text prompts* into `high-quality`, `photorealistic images`, pushing the boundaries of text-to-image generation.
- **Cartoonify**: Cartoonify is an AI model that transforms *real images into high-quality cartoon-style representations*, adding a `playful` and `artistic touch` to photographs and visuals.

> ***NOTE***: Processing may take more time than expected due to cold boot of Ai Models.

Feel free to add more models and documentation as needed.

## Output
Below are some of the images produced using this project.  

![OUTPUT 1](https://github.com/naveen61346134/ImageSynthX-Outputs/blob/main/asr.jpeg)
*Image produced using SDXL (can be used in combination with Real Esrgan to produce more high quality and sharpened image)*

![OUTPUT 2](https://github.com/naveen61346134/ImageSynthX-Outputs/blob/main/new.jpeg)
*Image produced using SDXL (can be used in combination with Real Esrgan to produce more high quality and sharpened image)*

![OUTPUT 3](https://github.com/naveen61346134/ImageSynthX-Outputs/blob/main/cat.jpeg)
*Image produced using SDXL (can be used in combination with Real Esrgan to produce more high quality and sharpened image)*

## Contributing

If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository on GitHub.

2. Create a new branch for your feature or bug fix.

3. Make your changes and commit them with clear and concise commit messages.

4. Push your changes to your fork.

5. Create a pull request to merge your changes into the main repository.

## License

This project is licensed under the [*GPL-3.0 License*](LICENSE).

---
