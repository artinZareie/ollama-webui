import cli
import ui
import ai_interface as ai
from pprint import pprint # TODO: imported for debugging. Remove later.

if __name__ == "__main__":
    pprint(ai.get_model_names(ai.list_models()))