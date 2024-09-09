from transformers import T5Tokenizer, T5ForConditionalGeneration

model_name = "google/flan-t5-base"

# Load the model and tokenizer
try:
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
except Exception as e:
    raise RuntimeError(f"Failed to load model or tokenizer: {e}")

def summarize_text(text):
    input_text = "summarize: " + text
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
    
    try:
        outputs = model.generate(
            inputs.input_ids,
            max_length=150,
            min_length=30,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        raise RuntimeError(f"Failed to generate summary: {e}")
    
    return summary
