from fastapi import APIRouter, HTTPException, status, Response
from app.models.api_models import Product
from app.crud.products import create_product, read_product, update_product, delete_product
from typing import Union
from util.translations import _

router = APIRouter()

def product_not_found_exception():
    """Raises an HTTP exception for not found products."""
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_("Product not found"))

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product_endpoint(product: Product) -> Product:
    """Create a new product."""
    await create_product(product)
    return product

@router.get("/{product_id}", response_model=Product)
async def read_product_endpoint(product_id: str) -> Union[Product, HTTPException]:
    """Retrieve a product by its ID."""
    product = await read_product(product_id)
    if not product:
        product_not_found_exception()
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product_endpoint(product_id: str, product: Product) -> Union[Product, HTTPException]:
    """Update a product by its ID."""
    updated_product = await update_product(product_id, product)
    if not updated_product:
        product_not_found_exception()
    return updated_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_endpoint(product_id: str) -> Response:
    """Delete a product by its ID."""
    success = await delete_product(product_id)
    if not success:
        product_not_found_exception()
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)
