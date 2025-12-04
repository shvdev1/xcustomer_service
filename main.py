from fastapi import FastAPI, HTTPException, Depends
from models import Customer
from db import CustomerORM, SessionLocal, engine, Base
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import asyncio

app = FastAPI()

# Create tables if not exist
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())


@app.post("/api/v1/customer", response_model=Customer)
async def add_customer(customer: Customer):
    async with SessionLocal() as session:
        db_customer = CustomerORM(name=customer.name)
        session.add(db_customer)
        await session.commit()
        await session.refresh(db_customer)
        return Customer(id=db_customer.id, name=db_customer.name)

@app.get("/api/v1/customer/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    async with SessionLocal() as session:
        result = await session.execute(select(CustomerORM).where(CustomerORM.id == customer_id))
        db_customer = result.scalar_one_or_none()
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return Customer(id=db_customer.id, name=db_customer.name)

@app.patch("/api/v1/customer/{customer_id}", response_model=Customer)
async def patch_customer(customer_id: int, customer: Customer):
    async with SessionLocal() as session:
        result = await session.execute(select(CustomerORM).where(CustomerORM.id == customer_id))
        db_customer = result.scalar_one_or_none()
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        db_customer.name = customer.name
        await session.commit()
        await session.refresh(db_customer)
        return Customer(id=db_customer.id, name=db_customer.name)

@app.delete("/api/v1/customer/{customer_id}")
async def delete_customer(customer_id: int):
    async with SessionLocal() as session:
        result = await session.execute(select(CustomerORM).where(CustomerORM.id == customer_id))
        db_customer = result.scalar_one_or_none()
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        await session.delete(db_customer)
        await session.commit()
        return {"detail": "Customer deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)