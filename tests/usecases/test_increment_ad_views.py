import pytest

from src.application.exceptions import AdNotFoundError
from src.application.usecases.create_ad import CreateAd
from src.application.usecases.increment_ad_views import IncrementAdViews
from tests.conftest import FakeUnitOfWork


@pytest.mark.asyncio
async def test_increment_views_success(
    fake_uow: FakeUnitOfWork,
) -> None:
    create = CreateAd(fake_uow)
    created = await create.execute(
        user_id=1,
        title="T",
        description="d",
        price=100,
        category="c",
        city="x",
    )

    increment = IncrementAdViews(fake_uow)

    assert created.views == 0
    await increment.execute(created.id)

    ad = await fake_uow.ads.get_by_id(created.id)
    assert ad is not None
    assert ad.views == 1

    await increment.execute(created.id)
    ad = await fake_uow.ads.get_by_id(created.id)
    assert ad is not None
    assert ad.views == 2


@pytest.mark.asyncio
async def test_increment_views_not_found(
    fake_uow: FakeUnitOfWork,
) -> None:
    increment = IncrementAdViews(fake_uow)

    with pytest.raises(AdNotFoundError):
        await increment.execute(999)
