from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import unittest
from selenium.webdriver.support.select import Select


class ShopTest(unittest.TestCase):

    def setUp(self):
        # Warunki wstępne
        self.driver = webdriver.Chrome()
        self.driver.get("https://fakestore.testelka.pl/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def testDiscountCode(self):

        shop_tab = self.driver.find_element(By.LINK_TEXT,'Sklep')
        shop_tab.click()

        windsurfing = self.driver.find_element(By.XPATH, '//a[@aria-label="Przejdź do kategorii produktu Windsurfing"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", windsurfing)
        windsurfing.click()

        # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # sleep(5)

        list_price = []
        list_id = []
        priceid_dic = {}
        ceny = self.driver.find_elements(By.XPATH, '//bdi')
        id = self.driver.find_elements(By.XPATH, '//a[@class="button product_type_simple add_to_cart_button ajax_add_to_cart"]')
        for d in id:
            id_value = d.get_attribute('data-product_id')
            list_id.append(id_value)
        print(list_id)

        for i in ceny:
            price = float((i.text[:-3]).replace(",", ".").replace(" ", ""))
            # print(price)
            list_price.append(price)
        print(list_price)

        priceid_dic = dict(zip(list_price, list_id))
        print(priceid_dic)

        for key in priceid_dic:
            if key < 3000:
                print(key)
                result = f'//a[@data-product_id="{priceid_dic[key]}"'
                print(result)
                choose = self.driver.find_element(By.XPATH, f'//a[@data-product_id="{priceid_dic[key]}"]')
                self.driver.execute_script("arguments[0].scrollIntoView();", choose)
                choose.click()




        # for p in list_price:
        #     if p > 5000:
        #         # choose = self.driver.find_element(By.XPATH, '//a[@class="button product_type_simple add_to_cart_button ajax_add_to_cart"]')
        #         choose = self.driver.find_element(By.XPATH, '//a[@data-product_id="391"]')
        #         self.driver.execute_script("arguments[0].scrollIntoView();", choose)
        #         choose.click()
        sleep(5)

        # choose = self.driver.find_element(By.XPATH, '//a[@data-product_id="393"]')
        # self.driver.execute_script("arguments[0].scrollIntoView();", choose)
        # choose.click()
        # # sleep(5)

        basket = self.driver.find_element(By.XPATH, '//a[contains(@title, "Zobacz koszyk")]')
        basket.click()
        # self.driver.execute_script("scroll(0, 0);")
        # sleep(5)

        coupon_input = self.driver.find_element(By.XPATH, '//input[@id="coupon_code"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", coupon_input)
        coupon_input.send_keys("windsurfing350")
        submit = self.driver.find_element(By.XPATH, '//button[@class="button"]')
        submit.click()
        # sleep(5)

        amount_of_prod = self.driver.find_element(By.XPATH, '//span[@class="count"]')
        new_amount = float(amount_of_prod.text[:1])
        print(type(new_amount))


        pomnozone = new_amount * 350
        print(pomnozone)

        wartosc_kuponu = '350,00 zł'
        kupon = self.driver.find_element(By.XPATH, '//td[@data-title="Kupon: windsurfing350"]/span[@class="woocommerce-Price-amount amount"]').text[:-3].replace(",", ".").replace(" ", "")
        kupon_int = float(kupon)
        print(kupon_int)
        self.assertEqual(kupon_int, pomnozone)


        message_notice = self.driver.find_element(By.XPATH, '//div[@class="woocommerce-message"]').text
        self.assertEqual("Kupon został pomyślnie użyty.", message_notice)
        print(message_notice)


        pass

    def tearDown(self):
        self.driver.quit()