from solution_parser import SolutionsParser
from import_solutions import ImportSolutions
import json

if __name__ == '__main__':
    # bases solutions
    # with open("incomplete_result.json", "w", encoding="utf-8") as file:
    #     parser = SolutionsParser()
    #     json.dump(parser.get_base_info_solutions(), file, indent=4)

    # start from bases solutions #####
    # with open("incomplete_result.json", "r", encoding="utf-8") as file:
    #     incomplete_result_json = json.load(file)
    #
    # with open("result.json", "w", encoding="utf-8") as file:
    #     parser = SolutionsParser()
    #     json.dump(parser.update_solutions_info(incomplete_result_json, safe_update=True), file, indent=4)
    #
    # start with the latest updated solution
    # with open("base_test.json", "r", encoding="utf-8") as file:
    #     incomplete_result_json = json.load(file)
    #
    # with open("result.json", "w", encoding="utf-8") as file:
    #     parser = SolutionsParser()
    #     json.dump(parser.update_solutions_info(incomplete_result_json, safe_update=True), file, indent=4)

    # import solutions
    with open("incomplete_result.json", "r", encoding="utf-8") as file:
        solutions = json.load(file)
        ImportSolutions().run(solutions)