def test():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC    
    import time
    import smtplib

    smtp_mail = "SEND MAIL FROM THIS GMAIL ACC "
    smtp_pass ="SMTP MAIL PASSWORD"
    send_adress = "GMAIL TO WHERE YOU WANNA SEND"
    trendyol_mail ="TRENDYOL ACC MAIL"
    trendyol_pass = "TRENDYOL ACC PASS."

    def send_mail(user_mail,to_adress,password,message):
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=user_mail,password=password)
        connection.sendmail(from_addr=user_mail,to_addrs=to_adress, msg=message)
        connection.close()
        
    def create_dict(name,price):
        return {name[i]:price[i] for i in range(len(price))}

    option = webdriver.ChromeOptions()


    option.add_experimental_option("detach",True)
    option.add_argument("--disable-notifications");
    option.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=option)

    driver.get("https://www.trendyol.com/")
    driver.maximize_window()
    wait = WebDriverWait(driver,10)
    element = wait.until(EC.element_to_be_clickable((By.ID,"Ürün-Detay---Attribute-Phase-1-Copy-9")))
    close_tag = driver.find_element(By.ID,"Ürün-Detay---Attribute-Phase-1-Copy-9")
    close_tag.click()

    log_in = driver.find_element(By.XPATH,'//*[@id="account-navigation-container"]/div/div[1]/div[1]/p')
    log_in.click()



    element = wait.until(EC.element_to_be_clickable((By.ID,"login-email")))

    mail = driver.find_element(By.ID,"login-email")
    mail.send_keys(trendyol_mail)

    password = driver.find_element(By.ID,"login-password-input")
    password.send_keys(trendyol_pass)

    password.send_keys(Keys.ENTER)
    time.sleep(5)
    element = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="account-navigation-container"]/div/a/div/p')))

    my_favs = driver.find_element(By.XPATH,'//*[@id="account-navigation-container"]/div/a/div/p')
    my_favs.click()
    time.sleep(5)

    price_list = []
    product_names_list = []
    prices = driver.find_elements(By.CSS_SELECTOR ,".favored-product-container .p-card-wrppr .prc-box-dscntd")
    product_names =  driver.find_elements(By.CSS_SELECTOR ,".favored-product-container .prdct-desc-cntnr-name")

    purchasable_prices = [1500,70,300,100,200,70,70,300,200]

    for product_name in product_names:
        product_name = product_name.text
        product_names_list.append(product_name)
    for price in prices:
        time.sleep(0.5)
        print(price.text.split(" ")[0])
        try:
            element_price = price.text.split(" ")[0]
        except:
            pass
        
        if "," in element_price:
            element_price = element_price.split(",")[0]
            if "." in element_price:
                element_price = element_price.replace(".","")
                price_list.append(int(element_price))
            else:
                price_list.append(int(element_price))

        else:
            if "." in element_price:
                element_price = element_price.replace(".","")
                price_list.append(int(element_price))
            else:
                price_list.append(int(element_price))
        
    current_price_dict =create_dict(product_names_list,price_list) 
    expected_price_dict = create_dict(product_names_list,purchasable_prices) 

    product_namesss =  driver.find_elements(By.CSS_SELECTOR ,".favored-product-container .p-card-wrppr a")


    for product_name in current_price_dict:
        if current_price_dict[product_name] <= expected_price_dict[product_name]:
            for product in product_names:
                if product.text == product_name:
                    product.click()
                    driver.switch_to.window(driver.window_handles[1])
                    element = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="product-detail-app"]/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[2]')))
                    got_it = driver.find_element(By.XPATH,'//*[@id="product-detail-app"]/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[2]')
                    got_it.click()
                    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-button-container .add-to-basket-button-text")))
                    add_basket = driver.find_element(By.CSS_SELECTOR, ".product-button-container .add-to-basket-button-text").click()
                    time.sleep(2)
                    goto_basket = driver.find_element(By.CSS_SELECTOR,".basket-preview .account-basket").click()
                    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,".pb-summary .pb-summary-approve")))
                    
                    aprove_basket = driver.find_element(By.CSS_SELECTOR,".pb-summary .pb-summary-approve").click()
                    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,".p-summary .approve-button-wrapper .ty-primary-btn")))
                    save_continue = driver.find_element(By.CSS_SELECTOR,".p-summary .approve-button-wrapper .ty-primary-btn").click()
                    element = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="p-layout"]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/span[2]')))
                    accept = driver.find_element(By.CSS_SELECTOR,".p-contracts-approve .p-checkbox-text").click()
                    finish_purchase = driver.find_element(By.CSS_SELECTOR,".p-summary .approve-button-wrapper")
                    message = f"Your production which name {product_name} has been ordered wih {current_price_dict[product_name]}"
                    send_mail(user_mail=smtp_mail,to_adress=send_adress,message=message,password=smtp_pass)               
                    print("message has been sent")
                    driver.switch_to.window(driver.window_handles[0])
                    current_price_dict.pop(product_name)
                    expected_price_dict.pop(product_name)
        
        else:
            print("this is not suitable to buy")




test()