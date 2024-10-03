# views.py
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from menu.models import Category, MenuItem
import csv
import io

@csrf_exempt  # Disable CSRF for this endpoint (consider security implications)
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file')

        if not csv_file:
            return JsonResponse({'error': 'No file provided'}, status=400)

        # Read the CSV file
        try:
            # Use pandas to read the CSV file
            df = pd.read_csv(csv_file)

            for index, row in df.iterrows():
                category_name = row['Category']
                item_name = row['Item'] 
                price = row['Price'] if pd.notna(row['Price']) else 0.0 
                event = row['Event']
                available = row['Availability']
                category, created = Category.objects.get_or_create(category_name=category_name)  
                print(f'{category.category_name} added')

                # Create the menu item
                menuitem = MenuItem.objects.create(
                    item_name=item_name,  
                    description=f"An item in the {category_name} category.",
                    price=float(price),
                    availability=bool(available),  
                    category=category,  
                    event=bool(event)
                )
                
                print(f'{menuitem.item_name} added')

            return JsonResponse({'message': 'Data uploaded successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
