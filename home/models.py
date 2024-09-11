from django.db import models
from django.contrib.auth.models import User


from utils.models import BaseModel
from .constants import MARITAL_STATUS_CHOICES, ADDRESS_CHOICES

class Address(models.Model):
    """
    Represents an address that can be associated with an owner or a home.
    """
    street_address = models.CharField(max_length=255, db_index=True)
    city = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=100, db_index=True)
    postal_code = models.CharField(max_length=20, db_index=True)
    country = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=ADDRESS_CHOICES,  default='Home', null=True, blank=True)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.postal_code}, {self.country}"

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        indexes = [
            models.Index(fields=['city', 'state']),
        ]
    
    @classmethod
    def create_address(cls, street_address, city, state, postal_code, country, type='Home'):
        """
        Creates a new Address instance and saves it to the database.

        Args:
            street_address (str): The street address of the location.
            city (str): The city of the location.
            state (str): The state of the location.
            postal_code (str): The postal code of the location.
            country (str): The country of the location.
            type (str): Type of the address

        Returns:
            Address: The newly created Address instance.
        """
        address = cls(
            street_address=street_address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            type=type
        )
        address.save()
        return address
        

class Owner(BaseModel):
    """
    Represents a homeowner who can own multiple homes.
    
    This model extends the built-in Django User model by adding additional 
    personal details related to the owner.
    """
    # Link to Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    
    # Basic personal information
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='Single')
    spouse_name = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='owner_profile_pics/', null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='owner_address')
    

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Owner"
        verbose_name_plural = "Owners"

    @classmethod
    def create(cls, user, phone_number, date_of_birth, occupation=None, marital_status='Single', spouse_name=None, profile_picture=None, address=None):
        """
        Creates a new Owner instance and saves it to the database.

        Args:
            user (User): The User instance associated with the owner.
            phone_number (str): The phone number associated with the owner.
            date_of_birth (date): The date of birth of the owner.
            occupation (str, optional): The occupation of the owner.
            marital_status (str, optional): The marital status of the owner.
            spouse_name (str, optional): The name of the owner's spouse.
            profile_picture (ImageField, optional): The profile picture of the owner.
            address (Address, optional): The Address instance associated with the owner.

        Returns:
            Owner: The newly created Owner instance.
        """
        owner = cls(
            user=user,
            phone_number=phone_number,
            date_of_birth = date_of_birth,
            occupation=occupation,
            marital_status=marital_status,
            spouse_name=spouse_name,
            profile_picture=profile_picture,
            address=address
        )
        owner.save()
        return owner
    
    
class Home(BaseModel):
    """
    Represents a home owned by a specific owner.
    
    Each home is linked to an owner and an address.
    """
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='homes')
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='home_address')
    date_of_purchase = models.DateField(null=True, blank=True)
    ownership_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)

    def __str__(self):
        return f"Home at {self.address}"

    class Meta:
        ordering = ['address__city', 'address__street_address']
    
    @classmethod
    def create(cls, owner, street_address, city, state, postal_code, country, purchase_date, ownership_percentage, type='Home'):
        """
        Creates a new Home instance along with its associated Address and saves it to the database.

        Args:
            owner (Owner): The Owner instance who owns the home.
            street_address (str): The street address of the home.
            city (str): The city of the home.
            state (str): The state of the home.
            postal_code (str): The postal code of the home.
            country (str): The country of the home.
            purchase_date (date): The purchase date of the home.
            price (Decimal): The price of the home.
            ownership_percentage (Decimal): The ownership percentage of the house
            type (str): The type of the address

        Returns:
            Home: The newly created Home instance.
        """
        # Create or retrieve the Address instance
        address, created = Address.objects.get_or_create(
            street_address=street_address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            type=type
        )

        # Create the Home instance
        home = cls(
            owner=owner,
            address=address,
            purchase_date=purchase_date,
            ownership_percentage=ownership_percentage
        )
        home.save()
        
        return home