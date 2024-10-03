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

            # Process each row in the DataFrame
            for index, row in df.iterrows():
                category_name = row['Category']
                drink_price = row['DRINK PRICE (GHC)']

                # Create or get the category
                category, created = Category.objects.get_or_create(name=category_name)

                # Create the menu item
                MenuItem.objects.create(
                    name=f"{category_name} Drink",  # You might want to customize this
                    description=f"A drink in the {category_name} category.",
                    price=drink_price,
                    available=True,
                    category=category
                )

            return JsonResponse({'message': 'Data uploaded successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
