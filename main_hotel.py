import pandas as pd

df = pd.read_csv("005 hotels.csv", dtype={"id":str})
df_cards = pd.read_csv("002 cards.csv", dtype=str).to_dict(orient="records")
df_card_security = pd.read_csv("003 card-security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id,"name"].squeeze()

    def available(self):
        """Check if a hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id,"available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("005 hotels.csv", index=False)

    def view_hotels(self):
        pass


class Spa:
    def __init__(self, agreement):
        self.agreement1 = agreement

    def validate(self):
        if self.agreement == "yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are your booking details.
        Name: {self.customer_name}
        Hotel: {self.hotel.name}
        """
        return content


class SpaTicket():
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def spa_generate(self):
        content1 = f""" 
        Thank you for your SPA reservation
        Here are your SPA booking details.
        Name: {self.customer_name}
        Hotel: {self.hotel.name}
        """
        return content1


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, cvc, holder):
        """Create another dictionary here as comparison for the cards df"""
        cards_data = {"number":self.number, "expiration":expiration, "cvc":cvc,
                      "holder": holder}
        if cards_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_card_security.loc[df_card_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


if __name__ == "__main__":
    print(df)
    hotel_ID = input("Enter the id of the hotel: ")
    hotel = Hotel(hotel_ID)

    if hotel.available():
        credit = SecureCreditCard(number="1234")
        if credit.validate(expiration="12/26", cvc="123", holder="JOHN SMITH"):
            if credit.authenticate(given_password="mypass"):
                hotel.book()
                name = input("Enter your name: ")
                reservation = ReservationTicket(name, hotel)
                print(reservation.generate())

                spa_package = input("Do you like to book a SPA package?")
                if spa_package == "yes":
                    spa = SpaTicket(customer_name=name, hotel_object=hotel)
                    print(spa.spa_generate())
                else:
                    print("Spa package was not selected!")
            else:
                print("Credit card authentication failed!")
        else:
            print("There was a problem with your payment!")
    else:
        print("Hotel is not free.")
