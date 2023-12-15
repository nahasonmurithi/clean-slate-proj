#!/usr/bin/env python3
import click
from models import Client, session, CleaningTask, ClientTask
import re

# working with rich text
from rich.table import Table, Column
from rich.console import Console
# 

def home_page(current_user_id):
    # fetch all tasks
    cleaning_tasks = session.query(CleaningTask).all()
    click.echo(cleaning_tasks)

    console = Console()

    table = Table(show_header=True, header_style="bold cyan")

    table.add_column("task_id", style='bold')
    table.add_column("task category", style='bold')
    table.add_column("price", style='bold')
    table.add_column("cleaner", style='bold')

    # fill table with fetched tasks
    for item in cleaning_tasks:
        # table.add_row(str(item.task_id), item.task_description
        #               )
        table.add_row(str(item.task_id), item.task_description,
                      str(item.price), item.cleaner.full_name)

    console.print(
        '''
        Listed below is a variety of services available to our esteemed customers.\n To book a cleaning service, select the id adjacent to the service then press enter''', style="bold green")

    console.print(table)

    selected_task_id = click.prompt("Please select task_id: ", type=int)

    if selected_task_id in range(1, (cleaning_tasks[-1].task_id+1)):
        client_task = ClientTask(
            client_id = current_user_id,
            task_id = selected_task_id
        )

        session.add(client_task)
        session.commit()


        for item in cleaning_tasks:
            if selected_task_id == item.task_id:
                console.print(
                        f"{item.task_description} service has been booked successfully!! {item.cleaner.full_name} will arrive at your premises in the next hour. Thank you for choosing clean slate😁", style="green")

        session.close()

    else:
        click.secho("Invalid task id! Please try again ", fr="red")
        home_page(current_user_id)

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
        home_page(user.client_id)
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
        home_page(client.client_id)
    else:
        click.secho(("Invalid email address"), fg="red")
        
    

if __name__ == '__main__':
    welcome()

