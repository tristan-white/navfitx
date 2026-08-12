from navfitx.models import Fitrep


def test_build_example_fitrep_returns_valid_fitrep() -> None:
    from navfitx.examples import build_validated_example_fitrep

    fitrep = build_validated_example_fitrep()
    Fitrep.model_validate(fitrep)


def test_build_example_fitrep_returns_fresh_instances() -> None:
    from navfitx.examples import build_validated_example_fitrep

    first = build_validated_example_fitrep()
    second = build_validated_example_fitrep()

    assert first is not second
