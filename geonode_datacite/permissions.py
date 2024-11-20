from geonode.security.handlers import BasePermissionsHandler
from geonode_datacite.models import DataCite
from geonode.security.permissions import VIEW_PERMISSIONS, DOWNLOAD_PERMISSIONS


class DataCitePermissionsHandler(BasePermissionsHandler):
    @staticmethod
    def fixup_perms(instance, perms_payload, *args, **kwargs):
        datacite = DataCite.objects.filter(resource=instance).first()
        if not datacite or (datacite.state != DataCite.State.findable.value):
            return perms_payload

        # if is findable, we need to remove the edit permissions
        # to everyone, only the admin can edit the resource
        user_perms = DataCitePermissionsHandler._adjust_user_perms(
            perms_payload["users"]
        )
        group_perms = DataCitePermissionsHandler._adjust_group_perms(
            perms_payload["groups"]
        )
        return {"users": user_perms, "groups": group_perms}

    @staticmethod
    def _adjust_user_perms(perms_payload):
        adjusted_payload = {}
        for user, perms in perms_payload.items():
            if not user.is_superuser:
                adjusted_payload.update(DataCitePermissionsHandler._give_perms(user))
            else:
                # if the user is admin, we should keep the permissions
                adjusted_payload[user] = perms
        return adjusted_payload

    @staticmethod
    def _adjust_group_perms(perms_payload):
        adjusted_payload = {}
        for group, _ in perms_payload.items():
            adjusted_payload.update(DataCitePermissionsHandler._give_perms(group))
        return adjusted_payload

    @staticmethod
    def _give_perms(obj):
        return {obj: VIEW_PERMISSIONS + DOWNLOAD_PERMISSIONS}
