About
------------
This is a tool for the data preparation stage for the [Github Customer Service Agent](https://github.com/silviachen46/RAG_CustomerAgent), a continuation of the great work by ima9428@rit.edu and ibrr1@hotmail.com.

A couple of functionalities added: This new work skips PRs and only crawls issue tickets to save up github api request usage.
Now it also crawls comment history, user actions(mentioning another PR or issues), and labels are now combined to generated in a single file. Also, it crawls all images in each ticket and pass to [the BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base) to convert to descriptive text as a part of the comment history.

Setting up tool:
--------------------
1. Add the repo(s) url which you want to crawl the issues for in github_issues_url.csv file
2. Open "extract.py" and add your Github credentials in line 17
3. Open terminal or command prompt.
4. Change the location to the tool location.
5. Type "pip install -r requirements.txt" to install all the packages that you need to run the tool.
6. Compile functions for crawling the tickets, downloading images from tickets, and converting the images to texts.
7. Run the general script by typing: python extract.py.
8. The tool will generate a single csv files containing all information.

Large-scale crawling for opensource repository:
--------------------
As github has [rate limit](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28) for REST api usage, which is 5000 requests an hour for authorized user with api token, here is the way to estimate:

number of api requests = (number of PRs + number of issues)/100 + number of issues

If this result exceeds 5000, you may want to register for multiple github accounts and create a list for your api tokens so you will be able to crawl them all in once.

A sample is given [here]()

