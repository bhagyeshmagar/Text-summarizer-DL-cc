from text_cleaner import clean_text

# Initialize global variable to hold the model and tokenizer
_model = None
_tokenizer = None

def get_summarizer_components():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        import warnings
        warnings.filterwarnings("ignore")
        
        model_name = "facebook/bart-large-cnn"
        print(f"Loading abstractive deep learning model ({model_name})...")
        print("This requires ~1.6GB memory and might take a moment on the first run.")
        
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        print("LLM Loaded Successfully!")
    return _tokenizer, _model

def main(text: str, max_length: int = 150, min_length: int = 40):
    """
    Abstractive Deep Learning summarization using BART.
    It reads the text, creates novel contextual sentences, and outputs it.
    """
    cleaned = clean_text(text)
    
    tokenizer, model = get_summarizer_components()
    
    # BART model has a max context length of 1024 tokens.
    # We safely truncate the input text during tokenization.
    inputs = tokenizer(cleaned, max_length=1024, return_tensors="pt", truncation=True)
    
    # Generate the abstractive summary
    summary_ids = model.generate(
        inputs["input_ids"], 
        max_length=max_length, 
        min_length=min_length, 
        num_beams=4,
        early_stopping=True,
        do_sample=False
    )
    
    summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    return summary