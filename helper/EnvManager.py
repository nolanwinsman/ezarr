import os


class EnvManager:
    def __init__(self, path=".env"):
        self.path = path
        self.env = self._load()
        self.dirty = False

    def _load(self):
        env = {}

        if not os.path.exists(self.path):
            return env

        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#") or "=" not in line:
                    continue

                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()

        return env

    # -----------------------------
    # CORE FEATURE YOU WANT
    # -----------------------------
    def require(self, key, prompt=None, optional=False, mask=True):
        value = self.env.get(key, "").strip()

        # If value exists, just return it
        if value:
            self._print_loaded(key, value, mask)
            return value

        # If optional and empty, allow skip
        if optional and not value:
            if prompt:
                print(f"{prompt} (optional, press enter to skip):", end=" ")
            else:
                print(f"{key} (optional):", end=" ")

            value = input().strip()
            self.env[key] = value
            self.dirty = True
            return value

        # Required field
        if not prompt:
            prompt = f"Enter {key}"

        print(f"{prompt}:", end=" ")
        value = input().strip()

        self.env[key] = value
        self.dirty = True
        return value

    def _print_loaded(self, key, value, mask):
        if not mask:
            print(f"{key} = {value}")
            return

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
            if any(x in k for x in ["TOKEN", "KEY", "SECRET"]):
                self._print_loaded(k, v, True)
            else:
                print(f"{k} = {v}")

    def save(self):
        if not self.dirty:
            return

        with open(self.path, "w") as f:
            for k, v in self.env.items():
                f.write(f"{k}={v}\n")

        self.dirty = False