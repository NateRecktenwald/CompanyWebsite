#most of the changes were small and made it so the user couldn't send bad requests to be parsed such as having 
#multiple '&' within their request I solved this by checking the length of the array after splitting the parameters
#which should fix the parsing error my previous code possesed



def setParams(params):
    global contacts
    name = ""
    email = ""
    birthdate = ""
    news = "All News"
    rumor = "no rumors"
    count = 2
    #convert url string to normal characters and split the parameters
    try:
        normParams = urllib.parse.unquote(params, encoding='utf-8', errors='replace')
    except:
        return 0
    vals = (normParams.split("&"))

    #this was added to prevent unparsable data sent through the contact log and will only proceed if the proper data style was submitted
    if(len(vals) > 4):
        return 0
    
    #this is the main portion of code that sets the variables for each part of the contact form
    for i in range(len(vals)):
        key = vals[i].split("=")[0]
        val = vals[i].split("=")[1]
        if key == "name":
            name += val.replace('+', ' ')
            count += 1
        elif key == "email":
            email = val
            count += 1
        elif key == "birthday":
            temp = val.split("-")
            if(val != ""):
                birthdate = temp[1] + "-" + temp[2] + "-" + temp[0]
        elif key == "news":
            news = val
        elif key == "rumors":
            if val == "on":
                rumor = "wants rumors"
            else:
                rumor = "no rumors"

    #this was added and will return a sucess if all of the required variables were present and false if otherwise
    if count == 4 and birthdate != "":
        contacts[name] = [email, birthdate, news, rumor]
        return 1
    else:
        return 0
    

