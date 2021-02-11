from selenium import webdriver
import os
import re

main_url="https://wis.ntu.edu.sg/webexe/owa/fyp_eee_student.list_projects?p1=xxx&p2=xxx&p_with_stats=Y%20"


#Initializes firefox driver for selenium
def init_driver():
    return webdriver.Firefox()



#Filters out links that contains blacklisted words
def blacklist_main(driver):
    status=True
    while status:
        filename=input("Copy paste file name here without file extension.\n")
        filename+=".txt"
        url_file=open(filename,"r")
        url_list=url_file.readlines()
        if not url_list:
            print("Empty file or does not exist.")
            return
        url_file.close()
        allwords=get_description_from_sites(url_list,driver)
        filtered_links=blacklist_filter(allwords,filename)
        userin=input("View filtered results? (Y/N)\n")
        userin=userin.lower()
        if userin =='y':
            for url in filtered_links:
                driver.get(url)
                print("Enter 'e' to stop viewing.")
                user_in=input("Press enter to view next website.\n")
                user_in=user_in.lower()
                if user_in=="e":
                    break
        userin=input("Blacklist another file? (Y/N)\n")
        userin=userin.lower()
        if userin=="n":
            status=False



#Checks if url link to be rejected
def blacklist_filter(dict_of_words,filename):
    
    print("Type in keywords you want to filter seperated by space.")
    user_in=input("Examples: software hardware\n")
    user_in=user_in.lower()
    blacklist=user_in.split()
    link_list=[]
    new_file=open("Filtered "+filename,"w")
    for url in dict_of_words:
        found=False
        for word in dict_of_words[url]:
            if word in blacklist:
                found=True
                break
        if not found:
            new_file.write(url)
            link_list.append(url)
    new_file.close()
    return link_list



#Get all project links from NTU Website
def get_list_of_links(driver):

    driver.get(main_url)

    table=driver.find_element_by_id('ui_body_container').find_elements_by_css_selector('center')[0]
    rows=table.find_elements_by_css_selector('tr')
    links=[]
    for row in rows[1:]:
        link=list(row.find_element_by_css_selector('a').get_attribute('href'))
        link=combine(link)
        links.append(link)
    return links



#Checks if keywords exists in the words from description
# --- ONLY USES SMALL LETTERS AND NUMBERS ---
def search(keywords,dict_of_words):
    url_list=[]
    found=False
    for key in dict_of_words:
        found=False
        for word in dict_of_words[key]:
            if word in keywords:
                found=True
                break
        if found:
            url_list.append(key)
    return url_list


#Splits paragraph into words for searching
def word_split(para):
    words=re.sub("[^\w]", " ", para).split()
    words=list(set(words))
    for i,word in enumerate(words):
        words[i]=word.lower()
    return words

    
#Combine letters into a string for http url
def combine(link_letters):
    res=""
    for letter in link_letters:
        res+=letter
    return res



#Goes to website
def get_description_from_sites(links,driver):
    dict_of_words={}
    for link in links:
        driver.get(link)
        para=""
        table=driver.find_element_by_id('ui_body_container').find_elements_by_css_selector('center')[0]
        search=table.find_elements_by_css_selector('tr')
        title=search[1].find_elements_by_css_selector('td')[1].text
        summary=search[2].find_elements_by_css_selector('td')[1].text
        para=title+" "+summary
        para=word_split(para)
        dict_of_words[link]=para
    return dict_of_words



#Continues to search links repeatedly by user command
def loop_to_search(allwords,driver):
    cmd=""
    print("To end this function, type '/end'.")
    while True:
        print("Type in keywords you want to search seperated by space.")
        user_in=input("Examples: software hardware\n")
        user_in=user_in.lower()
        if user_in=="/end":
            break
        cmd=user_in.split()
        search_hits=search(cmd,allwords)
        filename="Custom search for {}.txt".format(user_in)
        custom_file=open(filename,"w")
        user_in=input("Would you like to view the websites? (Y/N)\n")
        user_in=user_in.lower()
        if user_in=='y':
            for url in search_hits:
                driver.get(url)
                print("Enter 'e' to stop viewing.")
                print("Enter 's' to save current url.")
                user_in=input("Press enter to view next website.\n")
                user_in=user_in.lower()
                if user_in=="e":
                    break
                elif user_in=="s":
                    custom_file.write(url)
                    custom_file.write("\n")
        else:
            for url in search_hits:
                custom_file.write(url)
                custom_file.write("\n")                
        custom_file.close()

    print("Ending program...")


    
#Init main for debugging
def main():

    driver=init_driver()
    userin=input("Load blacklist mode? (Y/N)\n")
    userin=userin.lower()
    if userin=='y':
        blacklist_main(driver)
    else:
        links=get_list_of_links(driver)
        allwords=get_description_from_sites(links,driver)
        loop_to_search(allwords,driver)
    end(driver)
    

#Ends session
def end(driver):
    driver.quit()
    temp=input("Session ended and closed. Press any key to continue.")


    
#Main function
if __name__== "__main__":
    main()
