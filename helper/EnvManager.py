import os


class EnvManager:
    def __init__(self, path=".env"):
        self.path = path
        self.env = self._load()
        self.dirty = False

    # -------------------------
    # Load .env file
    # -------------------------
    def _load(self):
        env = {}

        if not os.path.exists(self.path):
            return env

        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#") or "=" not in line:
                    continue

                key, value = line.split("=", 1)
                env[key.strip()] = value.strip().strip('"').strip("'")

        return env

    # -------------------------
    # Save .env file
    # -------------------------
    def save(self):
        with open(self.path, "w") as f:
            for k in sorted(self.env.keys()):
                f.write(f"{k}={self.env[k]}\n")

        self.dirty = False

    # -------------------------
    # Get or prompt
    # -------------------------
    def get(self, key, prompt=None, mask=False):
        if key in self.env and self.env[key]:
            value = self.env[key]

            if mask:
                self._print_masked(key, value)

            return value

        value = input(f"{prompt}: ").strip()

        self.env[key] = value
        self.dirty = True   # ← IMPORTANT

    return value

    # -------------------------
    # Helpers
    # -------------------------
    def _print_masked(self, key, value):
        if len(value) > 10:
            print(f"{key} = {value[:6]}...{value[-4:]}")
        else:
            print(f"{key} = ***")

    def summary(self):
        if not self.env:
            print("No .env values found.")
            return

        print("\nLoaded environment variables:")

        for k, v in self.env.items():
            if "TOKEN" in k or "KEY" in k or "SECRET" in k:
                self._print_masked(k, v)
            else:
                print(f"  {k} = {v}")