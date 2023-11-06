from botasaurus.launch_tasks import launch_tasks
from botasaurus import *
import json
import datetime


url = "???"

class ScrapeHeadingTask(BaseTask):
    browser_config = BrowserConfig(
        profile="default",
    )
    def run(self, driver: BotasaurusDriver, data):

        driver.organic_get(url)

        answercell = driver.get_element_or_none_by_selector("#app > main > div.content-wrapper > div.page > section > div > table:nth-child(4) > tbody > tr:nth-child(1) > td.rounded-r-2.px-4.md\:px-5.py-3.font-bold", Wait.LONG)

        revealbutton = driver.get_element_or_none_by_selector("#app > main > div.content-wrapper > div.page > section > div > table:nth-child(4) > tbody > tr:nth-child(1) > td.rounded-r-2.px-4.md\:px-5.py-3.font-bold > button", Wait.LONG)

        revealbutton.click()

        answer = answercell.text
            
        return {
            "answer" : answer
        }
    

class GetEverything(BaseTask):
    browser_config = BrowserConfig(
        profile="default",
    )
    def run(self, driver: BotasaurusDriver, data):
    
        driver.organic_get(url)

        revealbutton = driver.get_element_or_none_by_selector("#app > main > div.content-wrapper > div.page > section > div > table:nth-child(4) > tbody > tr:nth-child(1) > td.rounded-r-2.px-4.md\:px-5.py-3.font-bold > button", Wait.LONG)

        revealbutton.click()

        rows = driver.get_elements_or_none_by_selector('table tr', Wait.LONG)

        table_data = []
        
        for row in rows:
            text = row.text
            if text.startswith("Date"):
                continue
            if text.startswith("Today\n"):
                text = text.replace("Today\n", "")
                # if " 799 " in text or text.endswith("PEACE"):
                #     break
                # if "2022" in text:
                #     break
            print(text)
            table_data.append(text)  
            
        return {
            "table_data" : table_data
        }


if __name__ == "__main__":
    launch_tasks(ScrapeHeadingTask)

    with open("./output/finished.json", "r") as f:
        data = json.load(f) 
        today_answer = data[0]["answer"]

    with open("./answers.json", "r") as f:
        answers = json.load(f)
    for key in answers:
        if answers[key] == today_answer:
            print(f"Already have {today_answer} for {key}")
            exit()
    answers[str(len(answers))] = today_answer
    answers = dict(sorted(answers.items(), key=lambda item: 0 - int(item[0])))
    with open("./answers.json", "w") as f:
        json.dump(answers, f, indent=4)
    with open("./answers.txt", "w") as f:
        for key in answers:
            wordle_date = datetime.datetime(2021, 6, 19) + datetime.timedelta(days=int(key))
            date =  wordle_date.strftime('%m-%d-%Y')
            f.write(f"{date} {key} {answers[key]}\n")



    # launch_tasks(GetEverything)
    # with open("./output/finished.json", "r") as f:
    #     data = json.load(f) 
    #     table_data = data[0]["table_data"]

    # answers = {}
    # for row in table_data:
    #     split_row = row.split(" ")
    #     answer = split_row[-1]
    #     number = split_row[-2]
    #     date = " ".join(split_row[:-2])
    #     answers[number] = {
    #         "answer": answer,
    #         "date": date
    #     }

    # with open("./output/answers.json", "w") as f:
    #     json.dump(answers, f, indent=4)