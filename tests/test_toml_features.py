from navfitx.models import Fitrep


def test_fitrep_toml_export(fitrep: Fitrep):
    # export a valid fitrep to toml str
    toml_str = fitrep.model_dump_toml()

    # convert toml str into fitrep
    new_fitrep = Fitrep.from_toml(toml_str)

    # confirm that fitrep is valid
    Fitrep.model_validate(new_fitrep)
