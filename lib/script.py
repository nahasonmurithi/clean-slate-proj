#!/usr/bin/env python3
import click
from models import Client, session
import re


@click.group()
@click.version_option(version="1.0", prog_name ="Clean Slate CLI")
def welcome():
    """Welcome to Clean Slate. \n
        To sign-in use the sign-in command \n
        ie. lib/script sign-in
    """
    welcome_message = """
===========================================================
Welcome to Clean Slate Services
Hello Client,
Thank you for choosing Clean Slate cleaning services. To handle your cleaning
deficiencies, we have a dedicated team of clinically diagnosed OCD cleaners
who find dirt revolting. You wont find a team dedicated to eradicating germs and
stains like this. We guarantee timely solutions to your dirt affairs and 
100% customer satisfaction. PS: hide you dirty thoughts in our premises as they too are
at risk of being disinfected away!
Regards,
Clean Slate Management
-----------------------------------------------------------------
    """
    click.secho((welcome_message), fg="blue", bold = True)
    
@welcome.command()
@click.option('--email', '-e', prompt="Enter your email address:")
@click.option('--password', '-p', prompt="Enter your password:", hide_input=True)
def sign_in(email, password):
    """Log in using email and password"""
    user = session.query(Client).filter_by(email = email, password = password).first()
    if user:
        click.secho(("Login successful"), fg="green")
    else:
        click.secho(("Login failed"), fg="red")

@welcome.command()
@click.option('--name', prompt=True)
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
@click.option('--contact_number', prompt=True)
def sign_up(name, email, password, contact_number):
    """Create a new account"""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    reg = re.compile(pattern)
    valid_email = reg.fullmatch(email)
    if valid_email:

        client= Client(
            client_name = name,
            email = email,
            password=password,
            contact_number=contact_number
        )

        session.add(client)
        session.commit()
        session.close()
        click.secho(("Account created successfully"), fg= "green")
    else:
        click.secho(("Invalid email address"), fg="red")
        
    

if __name__ == '__main__':
    welcome()

