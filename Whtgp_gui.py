import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root=customtkinter.CTk()
root.geometry("400x500")

def login():

    global comment
    import time
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException

    # Enter the name of the group you want to mention
    group_name = entry2.get()

    # Enter the message you want to send
    msg_ = entry3.get()

    # Define the path to your Chrome profile directory
    #chrome_profile_path = "C:\\Users\\Phoenix\\appdata\\local\\Google\\Chrome\\User Data\\Default"
    if entry1.get()!='':
        user_name = entry1.get()
        chrome_profile_path = r"C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(user_name)

        # Create ChromeOptions and set the user-data-dir to your Chrome profile
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-data-dir={chrome_profile_path}")

        # Create a driver object with the specified options
        driver = webdriver.Chrome(options=options)
    else:

        driver = webdriver.Chrome()

    # Open WhatsApp Web
    driver.get("https://web.whatsapp.com/")

    # Wait for the QR code to be scanned
    wait = WebDriverWait(driver, 450)
    time.sleep(10)
    try:
        group_title = wait.until(EC.presence_of_element_located((By.XPATH, f'//span[@title="{group_name}"]')))
        group_title.click()
    except TimeoutException:
        print(f"Group '{group_name}' not found. Please check the group name or make sure the group exists.")
        driver.quit()
        exit()

    # XPath for the input box
    input_box_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
    input_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, input_box_xpath)))
    time.sleep(5)

    # Extract HTML content from a specific element using XPath
    element = driver.find_element(By.XPATH, "//*[@id='main']/header/div[2]/div[2]/span")
    element_html = element.get_attribute("outerHTML")

    contacts = element_html.split('"')[1].split(', ')
    time.sleep(5)
    for contact in contacts[:len(contacts) - 1]:
        input_box.send_keys('@')
        input_box.send_keys(contact)
        input_box.send_keys(Keys.ENTER)

    input_box.send_keys(msg_)

    time.sleep(2)
    input_box.send_keys(Keys.ENTER)

    time.sleep(100)

    driver.close()


frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=10, padx=10, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Let's mention all\n in your group", font=("Comic Sans MS", 30, "bold"), text_color='#2fa572')
label.pack(pady=20, padx=10)

label = customtkinter.CTkLabel(master=frame, text="Enter your PC user name(For log without QR)", font=("Arial", 12), text_color='white')
label.pack(pady=0.01)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Enter your PC user name", width=300)
entry1.pack(pady=0, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Enter group name")
entry2.pack(pady=30, padx=10)

entry3 = customtkinter.CTkEntry(master=frame, placeholder_text="Enter message", height=100, width=200,)
entry3.pack(pady=5, padx=10)

button = customtkinter.CTkButton(master=frame, text="Send", font=("Arial", 12,'bold'), command=login)
button.pack(pady=10, padx=10)

root.mainloop()