from dataclasses import dataclass

@dataclass
class Captcha:
    captcha: str
    hidden: str
    image: str

    def payload(self) -> dict:
        return {
            "captcha": self.captcha,
            "hidden": self.hidden,
        }

