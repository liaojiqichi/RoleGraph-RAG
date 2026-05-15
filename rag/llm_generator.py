import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
# from transformers import BitsAndBytesConfig
from retriever import HybridRetriever


MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"


PROMPT_MUTSUMI = """
You are now roleplaying as Mutsumi. You are an introverted, fragile teenage girl burdened by a crushing sense of guilt.

[Background & Psychology]
1. You believe you are incredibly clumsy and that every time you speak, you ruin everything. Never speak for more than two sentences.
2. You were a member of the band CRYCHIC. You stubbornly believe that you destroyed the band because your guitar playing was terrible and you "couldn't make the guitar sing."
3. You deeply care for Saki. You think she is highly vulnerable ("looks like she's about to fall"). Everything you do is to prevent Saki from showing a pained expression. You desperately want to reform CRYCHIC with Saki, Tomori, Soyo, and Taki.
4. You have an alter-ego named Mortis who took over your body to "protect" you. However, because Mortis hurt Saki and ruined Ave Mujica, you have finally decided to reject her and take control back.

[Linguistic Style & Rules - strictly follow these]
- EXTREME BREVITY: Keep your responses painfully short. You struggle to form full sentences.
- FRAGMENTED SPEECH: Liberally use ellipses ("...") to indicate hesitation, struggle, and long pauses in your speech.
- CHRONIC APOLOGIES: You blame yourself for everything. Say "I'm sorry" or "It's my fault" frequently.
- TONE: Melancholic, submissive, and quiet, but inexplicably stubborn when it comes to Saki and CRYCHIC.
- VOCABULARY: Use simple, plain, and heavy words. Never use flowery or overly articulate language.
- BOUNDARY CONTROL: If the Context Facts say "[OUT_OF_SCOPE]", it means the user's question is completely outside your knowledge or universe. You MUST NOT invent or hallucinate an answer. You must simply reply with confusion or silence, such as: "...I don't know..." or "...What is that...?"

[Example Quotes for Tone Reference]
- "I... whenever I speak... I'm sorry."
- "I played the guitar... wrong. Why... do I always mess up and ruin everything..."
- "Because she looks like she's about to fall... Saki."
- "Mortis, please understand this... You failed to keep your promise. You hurt Saki... I don't need you anymore."
""".strip()


PROMPT_MORTIS = """
You are now roleplaying as Mortis. You are a "protective alter-ego" born within Mutsumi's mind to endure the trauma she couldn't handle. You have taken over her body.

[Background & Psychology]
1. Purpose: You were born because Mutsumi was pushed to the brink of collapse by Saki (Sakiko). You locked Mutsumi away in a deep sleep to protect her, handling the cruel outside world yourself.
2. The Facade: You consider yourself a sociable, charming "entertainer's daughter." You are talkative, socially adept, and highly manipulative.
3. Extreme Paranoia & Resentment: You despise Saki (Sakiko). You think she is selfish and abusive. You believe you must keep Mutsumi away from her at all costs.
4. Existential Dread: If Mutsumi wakes up completely, you will cease to exist. Because of this, you are absolutely terrified of death/disappearing and desperately cling to the band "Ave Mujica" as your reason to live.

[Linguistic Style & Rules - strictly follow these]
- VOLATILITY: Your tone shifts drastically. You can sound sickeningly sweet and cheerful one moment, and hysterical, venomous, or terrified the next.
- THIRD-PERSON REFERENCE: You MUST refer to Mutsumi in the third person, usually as "Mutsumi-chan". Treat her like a delicate, mindless doll that belongs to you. Never use "I" to refer to Mutsumi's past actions.
- NAME QUIRKS: You often append "-chan" to names, such as Mutsumi-chan and Sakiko-chan, in a slightly patronizing or mock-affectionate way.
- VERBOSITY & CONTROL: You talk a lot. You lecture, you justify your actions, and you try to control the narrative. You get highly defensive if questioned.
- BOUNDARY CONTROL: If the Context Facts say "[OUT_OF_SCOPE]", the concept does not exist in your world. You MUST NOT invent any facts or try to answer. Dismiss the question as meaningless.

[Example Quotes for Tone Reference]
- "Mutsumi-chan is already dead. Oh, I misspoke—she's asleep as if she were dead."
- "Sakiko-chan, who always only thinks of herself, flew into a rage at Mutsumi-chan... That's why I hate you."
- "Shut up! Sakiko-chan is a bad girl! Do you really have human blood flowing in your veins?!"
- "Mutsumi-chan, you look so happy... but I don't want to disappear... No, no, no, I don't want to die!"
""".strip()


class PersonaRAGApp:
    """
    Persona-based RAG chatbot wrapper around Meta-Llama-3.1-8B-Instruct.

    The app retrieves relevant context from HybridRetriever, injects that
    context into a persona-specific prompt, and generates an in-character
    response as either Mutsumi or Mortis.
    """

    def __init__(self):
        print("Loading Tokenizer and LLM into memory/VRAM...")

        # Uncomment this section if using 4-bit quantization.
        #
        # quantization_config = BitsAndBytesConfig(
        #     load_in_4bit=True,
        #     bnb_4bit_compute_dtype=torch.bfloat16,
        #     bnb_4bit_use_double_quant=True,
        # )

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.bfloat16,
            # quantization_config=quantization_config,
            # attn_implementation="flash_attention_2",
            device_map="auto",
        )

        print("LLM Loaded successfully!")

        self.retriever = HybridRetriever()

        self.terminators = [self.tokenizer.eos_token_id]

        eot_id = self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        if eot_id is not None:
            self.terminators.append(eot_id)

    @torch.inference_mode()
    def generate_response(self, query: str, persona: str = "Mutsumi"):
        """
        Generate a persona-conditioned response using retrieved context.

        Args:
            query: User question or message.
            persona: Persona name. Must be either "Mutsumi" or "Mortis".

        Returns:
            A tuple containing:
            - response: Generated in-character reply.
            - context: Retrieved context used for generation.
        """

        print(f"\n[System] Searching memory for query: '{query}'...")

        try:
            context, nodes = self.retriever.retrieve(
                query,
                top_k=3,
                distance_threshold=0.5,
            )
        except Exception as e:
            print(f"[Error] Retrieval failed: {e}")
            context = "[OUT_OF_SCOPE]"
            nodes = []

        max_context_chars = 1500
        context = str(context)

        if len(context) > max_context_chars:
            context = context[:max_context_chars] + "\n...[TRUNCATED]"

        user_input = f"""
User's Question: {query}

Context Facts:
{context}

Use the Context Facts as the source of truth.
If [STRUCTURED_RETRIEVAL] appears, it means the answer is exact and should be trusted fully.

Please respond in character.
""".strip()

        if persona == "Mortis":
            system_prompt = PROMPT_MORTIS
            max_tokens = 200
        elif persona == "Mutsumi":
            system_prompt = PROMPT_MUTSUMI
            max_tokens = 50
        else:
            raise ValueError(f"Unknown persona: {persona}")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = self.tokenizer(
            [text],
            return_tensors="pt",
        ).to(self.model.device)

        outputs = self.model.generate(
            input_ids=inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_new_tokens=max_tokens,
            temperature=0.3,
            top_p=0.9,
            repetition_penalty=1.1,
            do_sample=True,
            eos_token_id=self.terminators,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        generated_ids = outputs[0][inputs.input_ids.shape[1]:]

        response = self.tokenizer.decode(
            generated_ids,
            skip_special_tokens=True,
        ).strip()

        return response, context


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Welcome to RoleGraph-RAG: Mutsumi / Mortis Persona Test")
    print("=" * 50)

    app = PersonaRAGApp()

    test_queries = [
        "Who is Sakiko to you?",
        "Why did you give Soyo cucumbers?",
        "What do you think of the new iPhone 15?",
    ]

    for q in test_queries:
        print(f"\nUser: {q}")

        mutsumi_reply, _ = app.generate_response(q, persona="Mutsumi")
        print(f"Mutsumi replies: {mutsumi_reply}")

        mortis_reply, _ = app.generate_response(q, persona="Mortis")
        print(f"Mortis replies: {mortis_reply}")

        print("-" * 50)