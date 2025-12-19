# nodes.py (versi aman)

import re
import random

def is_balanced(text):
    """Cek apakah jumlah { dan } seimbang."""
    open_count = text.count('{')
    close_count = text.count('}')
    return open_count == close_count

def sanitize_unbalanced(text):
    """Opsional: coba perbaiki atau beri tahu pengguna."""
    # Di sini kita cukup kembalikan apa adanya, tapi log peringatan.
    print(f"[Spintax Warning] Input tidak seimbang: {text[:50]}...")
    return text

class SpintaxSpinnerNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "spintax_text": ("STRING", {"multiline": True, "default": "{Halo|Hai} dunia!"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "spin"
    CATEGORY = "utils/text"

    def spin(self, spintax_text, seed):
        random.seed(seed)
        
        # Validasi dasar
        if not is_balanced(spintax_text):
            # Opsional: coba lanjutkan dengan teks apa adanya, atau kembalikan error string
            result = sanitize_unbalanced(spintax_text)
            return (result,)

        result = self._spin_safe(spintax_text)
        return (result,)

    def _spin_safe(self, text, max_iter=100):
        """Spin dengan batas iterasi aman."""
        iter_count = 0
        while '{' in text and '}' in text:
            if iter_count >= max_iter:
                print("[Spintax Error] Melebihi batas iterasi — kemungkinan spintax rusak.")
                return text  # kembalikan apa adanya

            # Cari grup {...} paling dalam (tanpa { atau } di dalam)
            new_text = re.sub(r'\{([^{}]*)\}', lambda m: self._choose_random(m.group(1)), text)

            # Jika tidak ada perubahan, berhenti (mencegah loop)
            if new_text == text:
                break

            text = new_text
            iter_count += 1

        return text

    def _choose_random(self, options_str):
        if not options_str.strip():
            return ""
        options = [opt.strip() for opt in options_str.split('|')]
        return random.choice(options)


NODE_CLASS_MAPPINGS = {
    "SpintaxSpinner": SpintaxSpinnerNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SpintaxSpinner": "Spintax Spinner"
}