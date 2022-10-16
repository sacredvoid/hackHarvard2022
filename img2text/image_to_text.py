# from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
# import torch
# from PIL import Image
# import argparse

# model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
# feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
# tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# # setting the parameters
# max_length = 16
# num_beams = 4
# gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

# def predict_step(image_path):
#     i_image = Image.open(image_path)
    
#     # convert image ot RGB if not in RGB
#     if i_image.mode != "RGB":
#         i_image = i_image.convert(mode = "RGB")
    
#     images = [i_image]
    
#     # extracting the pixel values from the image and sending them to the cpu for further computation
#     pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
#     pixel_values = pixel_values.to(device)
    
#     # generating the encoded data of the pixel values
#     output_ids = model.generate(pixel_values, **gen_kwargs)

#     # decoding the data by tokenizing
#     preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
#     preds = [pred.strip() for pred in preds]
    
#     return preds[0]

# if __name__ == "__main__":

#     parser = argparse.ArgumentParser(description="Fetches the input image path")

#     parser.add_argument('-i','--input_image',type=str,required=True)

#     args = parser.parse_args()

#     img_captioning = predict_step(args.input_image)
