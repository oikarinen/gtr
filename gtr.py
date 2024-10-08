# Copyright (c) 2024 oikarinen

from argparse import ArgumentParser, Namespace

from google.cloud import translate_v2 as translate
from google.auth.exceptions import GoogleAuthError
from typing import NoReturn, Sequence

import errno
import logging
import sys


class Translator:
    """
    Translator class to translate text using Google Cloud Translation API.
    """

    def __init__(self) -> NoReturn:
        self.args: Namespace = Namespace()
        self.log = logging.getLogger(__name__)
        self.client = translate.Client()

    def translate(self, text: str) -> dict:
        """Translate text to target language."""

        if isinstance(text, bytes):
            text = text.decode("utf-8")
        return self.client.translate(text,
                                     target_language=self.args.target_language)

    def list_supported_languages(self) -> dict:
        """List supported languages."""
        return self.client.get_languages()

    def output(self, result: dict) -> NoReturn:
        """Output the translation result. """
        print("---------")
        print("Text: {}".format(result["input"].rstrip("\n")))
        print("Detected source language: {}".format(
            result["detectedSourceLanguage"].rstrip("\n")))
        print("Translation: {}".format(result["translatedText"].rstrip("\n")))
        print(f"Target language: {self.args.target_language}")
        print("---------")

    def main(self, args: Sequence[str] | None = None) -> int:
        """Entry point for the Translator class."""
        self.args = args
        try:
            if self.args.target_language not in self.list_supported_languages(
            ):
                self.log.error("Invalid target language")
                return 1

            if self.args.filename == "-":
                print("Enter text to translate, Ctrl-D to finish:")
                for line in sys.stdin:
                    if not line:
                        break
                    self.output(self.translate(line))
            else:
                with open(self.args.filename, "r") as f:
                    for line in f:
                        self.output(self.translate(line))

        except GoogleAuthError as ex:
            self.log.error("Google Auth Error: {}".format(ex))
            return 1
        except OSError as ex:
            if ex.errno != errno.EPIPE:
                raise
            self.log.error("Broken pipe")
            return 13
        except KeyboardInterrupt:
            self.log.error("Keyboard interrupt")
            return 2

        return 0


def main() -> NoReturn:
    """Parse command line arguments and call the Translator class."""
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)

    parser = ArgumentParser(prog="gtr", description="Google Translator")
    parser.add_argument("-t",
                        "--target-language",
                        type=str,
                        default="en",
                        help="Target language")
    parser.add_argument("-f",
                        "--file",
                        type=str,
                        dest="filename",
                        help="File to translate or '-' for stdin",
                        default="-")
    args = parser.parse_args()

    if not args.filename:
        parser.print_help()
        sys.exit(0)

    sys.exit(Translator().main(args=args))


if __name__ == "__main__":
    main()
