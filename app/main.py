from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database import get_connection


app = FastAPI(
    title="ReleaseForge Order API",
    version="0.2.0",
)


class OrderCreate(BaseModel):
    product: str
    quantity: int


class Order(BaseModel):
    id: UUID
    product: str
    quantity: int
    status: str


@app.get("/healthz")
def healthz():
    return {"status": "alive"}


@app.get("/ready")
def ready():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

        return {"status": "ready"}

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="database unavailable",
        )


@app.post("/orders", response_model=Order, status_code=201)
def create_order(order_request: OrderCreate):
    if order_request.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="quantity must be greater than zero",
        )

    order_id = uuid4()

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO orders (id, product, quantity, status)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        order_id,
                        order_request.product,
                        order_request.quantity,
                        "CREATED",
                    ),
                )

        return Order(
            id=order_id,
            product=order_request.product,
            quantity=order_request.quantity,
            status="CREATED",
        )

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="database unavailable",
        )


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: UUID):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, product, quantity, status
                    FROM orders
                    WHERE id = %s
                    """,
                    (order_id,),
                )

                row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="order not found",
            )

        return Order(
            id=row[0],
            product=row[1],
            quantity=row[2],
            status=row[3],
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="database unavailable",
        )