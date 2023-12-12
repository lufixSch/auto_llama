import os
from uuid import uuid4
import subprocess as sp
import re


class CodeExecutor:
    def __init__(self, data_path: str, image_path: str, code_path: str) -> None:
        self.data_path = os.path.abspath(data_path)
        self.image_path = os.path.abspath(image_path)
        self.code_path = os.path.abspath(code_path)

    def _format_code(self, code: str) -> tuple[str, list[str]]:
        """
        Reformat the code in order to capture outputs like plots or csv files.
        """

        formatted_code = ""

        # Replace plt.show() with plt.savefig(f"{image_path}/{uuid4().hex}.png")
        image_ids = []

        for line in code.splitlines():
            if "plt.show(" in line:
                id = f"{uuid4().hex}.png"
                formatted_code += (
                    re.sub(
                        r"plt\.show\(\)",
                        f'plt.savefig("{self.image_path}/{id}")',
                        line,
                    )
                    + "\n"
                )

                image_ids.append(id)
            else:
                formatted_code += line + "\n"

        return (formatted_code, image_ids)

    def _exec_code(self, code: str, id: str) -> str:
        """
        Execute provided code
        """

        file_path = os.path.join(self.code_path, f"{id}.py")

        # Create file and write code to it
        with open(file_path, mode="x") as f:
            f.write(code)

        # Execute code and capture output
        res = sp.check_output(["python3", file_path], cwd=self.data_path)

        return res.decode("utf-8")

    def run(self, code: str):
        """
        Format and execute the given code. Return ouput data and text.
        """

        id = uuid4().hex

        code, image_ids = self._format_code(code)
        out = self._exec_code(code, id)

        return {"id": id, "response": out, "images": image_ids}
