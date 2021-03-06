import asyncio
import inspect

from graphql import ExecutionResult


async def test__books_added_subscription__ok(schema):
    query = """
    subscription Books {
      booksAdded
    }
    """

    subscription = await schema.subscribe(query)
    assert hasattr(subscription, "iterator")
    assert inspect.isasyncgen(subscription.iterator)

    mutation = """
    mutation BooksMutation {
      createBooks(books: [{authorId: "MQ==", title: "New bookx"}])
    }
    """

    async def on_message():
        message = await subscription.__anext__()
        return message

    task = asyncio.create_task(on_message())
    await asyncio.sleep(0.1)
    result = await schema.run(mutation)
    subscription_result = await asyncio.wait_for(task, 5)

    assert isinstance(result, ExecutionResult)
    assert isinstance(subscription_result, ExecutionResult)

    assert result.data["createBooks"] == subscription_result.data["booksAdded"]


async def test__authors_added_subscription__ok(schema):
    query = """
    subscription Authors {
      authorsAdded
    }
    """

    subscription = await schema.subscribe(query)
    assert hasattr(subscription, "iterator")
    assert inspect.isasyncgen(subscription.iterator)

    mutation = """
    mutation AuthorsMutation {
      createAuthors(
        authors: {
          name: "Test"
          geo: { longitude: 40.123123124, latitude: -45.125551222 }
        }
      )
    }
    """

    async def on_message():
        message = await subscription.__anext__()
        return message

    task = asyncio.create_task(on_message())
    await asyncio.sleep(0.1)
    result = await schema.run(mutation)
    subscription_result = await asyncio.wait_for(task, 5)

    assert isinstance(result, ExecutionResult)
    assert isinstance(subscription_result, ExecutionResult)

    assert result.data["createAuthors"] == subscription_result.data["authorsAdded"]
