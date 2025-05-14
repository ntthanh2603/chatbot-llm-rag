from transformers import PhobertTokenizer

def tokenize_and_count(file_path):
    tokenizer = PhobertTokenizer.from_pretrained('vinai/phobert-base-v2')

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    tokens = tokenizer.tokenize(text)

    num_tokens = len(tokens)

    print(f"Number of tokens in the file: {num_tokens}")
    return num_tokens

file_path = 'crawl/data_vnu_member_university.txt'
tokenize_and_count(file_path)

# Note: Phobert requires input text must be segmented into words. 
# (e.g., "Chúng tôi là những nghiên cứu viên ." -> "Chúng_tôi là những nghiên_cứu_viên .")

# Reference: VNCoreNLP (using pip3 install py-vncorenlp)

# import os
# import py_vncorenlp
# if not os.path.exists('util/vncorenlp'):
#     os.makedirs('util/vncorenlp')
# # Automatically download VnCoreNLP components from the original repository
# # and save them in some local machine folder
# py_vncorenlp.download_model(save_dir='util/vncorenlp')

# # Load the word and sentence segmentation component
# rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='util/vncorenlp')

# text = 'Chúng tôi là những nghiên cứu viên .'

# output = rdrsegmenter.word_segment(text)

# print(output)
# ['Chúng_tôi là những nghiên_cứu_viên .']



# But when using the VnCoreNLP library, you need to download the models manually.
# BASE_URL1="https://github.com/vncorenlp/VnCoreNLP/master/models/wordsegmenter/vi-vocab"
# BASE_URL2="https://github.com/vncorenlp/VnCoreNLP/master/models/wordsegmenter/wordsegmenter.rdr"
# BASE_URL3="https://github.com/vncorenlp/VnCoreNLP/master/VnCoreNLP-1.2.jar"
