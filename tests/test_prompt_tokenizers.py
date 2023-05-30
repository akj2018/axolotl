import json
import logging
import unittest

from transformers import AutoTokenizer

from axolotl.prompt_tokenizers import ShareGPTPromptTokenizingStrategy
from axolotl.prompters import ShareGPTPrompter

logging.basicConfig(level="INFO")


class TestPromptTokenizationStrategies(unittest.TestCase):
    def setUp(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained("huggyllama/llama-7b")
        self.tokenizer.add_special_tokens(
            {
                "bos_token": "<s>",
                "eos_token": "</s>",
                "unk_token": "<unk>",
            }
        )

    def test_sharegpt_integration(self):
        with open("./fixtures/conversation.json", "r") as fin:
            data = fin.read()
            conversation = json.loads(data)
        with open("./fixtures/conversation.tokenized.json", "r") as fin:
            data = fin.read()
            tokenized_conversation = json.loads(data)
        prompter = ShareGPTPrompter("chat")
        strat = ShareGPTPromptTokenizingStrategy(
            prompter,
            self.tokenizer,
            False,
            2048,
        )
        example = strat.tokenize_prompt(conversation)
        for fields in ["input_ids", "attention_mask", "labels"]:
            self.assertEqual(len(example[fields]), len(tokenized_conversation[fields]))
            self.assertEqual(example[fields], tokenized_conversation[fields])


if __name__ == "__main__":
    unittest.main()