# from traceback import TracebackException
# from dateutil.utils import today
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
import unittest
# from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from faker import Faker
# import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime




given_value = float(input("Select all products up to value: "))
fake = Faker("pl_PL")

class ShopTest(unittest.TestCase):

    def setUp(self):
        # Warunki wstępne
        self.driver = webdriver.Chrome()
        self.driver.get("https://fakestore.testelka.pl/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        sleep(2)
        self.find_click('//a[@class="woocommerce-store-notice__dismiss-link"]')


    def testDiscountCode(self):

        shop_tab = self.driver.find_element(By.LINK_TEXT,'Sklep')
        shop_tab.click()

        self.find_click('//a[@aria-label="Przejdź do kategorii produktu Windsurfing"]')
        # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        list_price = []
        list_id = []

        value = self.driver.find_elements(By.XPATH, '//bdi')
        id = self.driver.find_elements(By.XPATH, '//a[@class="button product_type_simple add_to_cart_button ajax_add_to_cart"]')
        for d in id:
            id_value = d.get_attribute('data-product_id')
            list_id.append(id_value)
        # print(list_id)

        for i in value:
            price = float((i.text[:-3]).replace(",", ".").replace(" ", ""))
            list_price.append(price)
        # print(list_price)

        price_id_dic = dict(zip(list_price, list_id))
        # print(price_id_dic)


        for key in price_id_dic:
            if key <= given_value:
                # print(key)
                # result = f'//a[@data-product_id="{price_id_dic[key]}"'
                # print(result)
                self.find_click(f'//a[@data-product_id="{price_id_dic[key]}"]')

        try:
            self.find_click('//a[contains(@title, "Zobacz koszyk")]')


            coupon_input = self.driver.find_element(By.XPATH, '//input[@id="coupon_code"]')
            self.driver.execute_script("arguments[0].scrollIntoView();", coupon_input)
            coupon_input.send_keys("windsurfing350")
            submit = self.driver.find_element(By.XPATH, '//button[@class="button"]')
            submit.click()
            # sleep(5)

            amount_of_prod = self.driver.find_element(By.XPATH, '//span[@class="count"]')
            new_amount = float(amount_of_prod.text[:1])
            # print(type(new_amount))

            discount = new_amount * 350
            # print(discount)

            kupon = self.driver.find_element(By.XPATH, '//td[@data-title="Kupon: windsurfing350"]/span[@class="woocommerce-Price-amount amount"]').text[:-3].replace(",", ".").replace(" ", "")
            kupon_int = float(kupon)
            print('\n',kupon_int)
            self.assertEqual(kupon_int, discount)

            message_notice = self.driver.find_element(By.XPATH, '//div[@class="woocommerce-message"]').text
            self.assertEqual("Kupon został pomyślnie użyty.", message_notice)
            print(message_notice)

        except NoSuchElementException:

            element_to_hover_over = self.driver.find_element(By.ID, "site-header-cart")
            hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
            hover.perform()

            empty_basket = self.driver.find_element(By.XPATH, '//p[@class="woocommerce-mini-cart__empty-message"]').text
            self.assertEqual("Brak produktów w koszyku.", empty_basket)
            print(empty_basket)

    def tearDown(self):
        self.driver.quit()

    def testPayment(self):

        shop_tab = self.driver.find_element(By.LINK_TEXT,'Sklep')
        shop_tab.click()


        self.find_click('//a[@aria-label="Przejdź do kategorii produktu Wspinaczka"]')
        self.find_click('//span[@class="onsale"]')
        self.find_click('//button[@class="single_add_to_cart_button button alt"]')
        self.find_click('//a[@class="cart-contents"]')
        self.find_click('//a[@class="checkout-button button alt wc-forward"]')

        card_nr = 4242424242424242
        data = fake.date_time_between(start_date='-5y',  end_date='+5y')
        data_edit = datetime.strftime(data, "%m/%y")
        now = datetime.now()


        self.find_send("billing_first_name", fake.first_name())
        self.find_send("billing_last_name", fake.last_name())
        self.find_send("billing_address_1", fake.address())
        self.find_send("billing_postcode", fake.postalcode())
        self.find_send("billing_city", fake.city())
        self.find_send("billing_phone", fake.phone_number())
        self.find_send("billing_email", fake.email())


        # print(card_nr)
        iframe = self.driver.find_element(By.XPATH, '//iframe[@title="Bezpieczne pole wprowadzania numeru karty"]')
        self.driver.switch_to.frame(iframe)
        karta = self.driver.find_element(By.XPATH, '//input[@name="cardnumber"]')
        karta.send_keys(card_nr)
        self.driver.switch_to.default_content()
        sleep(2)

        # print(data)
        # print(now)
        # print(data_edit)

        iframe = self.driver.find_element(By.XPATH, '//iframe[@title="Bezpieczne pole wprowadzania terminu ważności"]')
        self.driver.switch_to.frame(iframe)
        exp_data = self.driver.find_element(By.XPATH, '//input[@name="exp-date"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", exp_data)
        exp_data.send_keys(data_edit)
        self.driver.switch_to.default_content()
        sleep(1)
        self.driver.save_screenshot("screen.png")

        # print(nr_cvc)
        iframe = self.driver.find_element(By.XPATH, '//iframe[@title="Bezpieczne pole wprowadzania CVC"]')
        self.driver.switch_to.frame(iframe)
        cvc= self.driver.find_element(By.XPATH, '//input[@name="cvc"]')
        cvc.send_keys(fake.credit_card_security_code())
        self.driver.switch_to.default_content()
        sleep(1)

        self.find_click('//input[@id="terms"]')

        self.find_click('//button[@id="place_order"]')


        if data < now:
            expired = self.driver.find_element(By.XPATH, '//div[@class="stripe-source-errors"]')
            expired_yes = (expired.is_displayed())
            self.assertTrue(expired_yes)

        else:
            order_done = WebDriverWait(self.driver,10).until(EC.text_to_be_present_in_element((By.XPATH, '//h1[@class="entry-title"]'),"Zamówienie otrzymane"))
            # zamowienie_done = self.driver.find_element(By.XPATH, '//header[@class="entry-header"]/h1[@class="entry-title"]').text
            # print(zamowienie_done)
            # print(order_done)
            # self.assertEqual("Zamówienie otrzymane", zamowienie_done)
            self.assertTrue(order_done)


    def tearDown(self):
        self.driver.quit()

    def find_send(self, where, what):
            find = self.driver.find_element(By.ID, where)
            find.send_keys(what)
            sleep(1)

    def find_click(self, path):
        find_button = self.driver.find_element(By.XPATH, path)
        self.driver.execute_script("arguments[0].scrollIntoView();", find_button)
        find_button.click()
        sleep(2)

