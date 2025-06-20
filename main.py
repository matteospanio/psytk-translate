from __future__ import annotations
from jinja2 import Environment, PackageLoader, select_autoescape
import argparse
import yaml
from typing import NoReturn
from dataclasses import dataclass
from pathlib import Path
import sys
import os


TRANSLATIONS_DIR = Path('languages')
AVAILABLE_LANGUAGES = [lang.stem for lang in TRANSLATIONS_DIR.glob('*.yml')]


@dataclass
class Translation:
    questions: dict
    answers: dict

    @classmethod
    def from_yaml(cls, file_path: Path) -> Translation:
        with file_path.open('r') as file:
            data = yaml.safe_load(file)
        return cls(questions=data['questions'], answers=data['answers'])


def get_translation(lang: str) -> Translation:
    return Translation.from_yaml(TRANSLATIONS_DIR / f'{lang}.yml')


env = Environment(
    loader=PackageLoader('main'),
    autoescape=select_autoescape()
)
template = env.get_template('quiz.psytk.jinja2')


def main(args) -> NoReturn:
    try:
        translations = get_translation(args.lang)
    except FileNotFoundError:
        print(f'Error: Translation file for language "{args.lang}" not found. Available languages: {", ".join(AVAILABLE_LANGUAGES)}')
        sys.exit(os.EX_OSFILE)

    output = template.render(questions=translations.questions, answers=translations.answers)
    
    if args.output:
        try:
            with open(f'{args.output}', 'w') as file:
                file.write(output)
            print(f'Quiz compiled successfully in {args.lang} language.')
        except IOError as e:
            print(f'Error writing to output file: {e}')
            sys.exit(os.EX_IOERR)
    else:
        print(output)
    
    sys.exit(os.EX_OK)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compile quiz template with translations.')
    parser.add_argument('--lang', '-l', type=str, help='Language code for translations', choices=AVAILABLE_LANGUAGES, required=True)
    parser.add_argument('--output', '-o', type=str, help='Output file name', required=False)
    args = parser.parse_args()
    main(args)
