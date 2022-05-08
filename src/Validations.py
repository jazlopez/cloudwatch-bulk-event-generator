import click


class Validations:

    """
    """


    @staticmethod
    def validate_total_events(ctx, option, value):
        """
        :param ctx:
        :param option:
        :param value:
        :return:
        """

        error = ""
        if value <= 0:
            error = "should be greater than 0"
        if value >= 10000:
            error = "should be less than 10000"

        if len(error):
            raise click.BadParameter(error)

        click.secho(f"[INFO] valid {option.name} argument: {value}")

        return value

    @staticmethod
    def validate_event_method(ctx, option, value):

        """
        :param ctx:
        :param option:
        :param value:
        :return:
        """

        error = ""
        ok_options = ['POST', 'GET', 'DELETE', 'PUT', 'PATCH']

        if value not in ok_options:
            error = f"{option.name} should be any of {'.'.join(ok_options)}"

        if len(error):
            raise click.BadParameter(error)

        click.secho(f"[INFO] valid {option.name} argument: {value}")
