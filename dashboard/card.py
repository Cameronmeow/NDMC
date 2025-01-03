from streamlit_elements import mui
from .dashboard import Dashboard


class Card(Dashboard.Item):
    LYMPHODEMA = ("Lymphedema is a chronic condition that causes swelling in the body's tissues due to a buildup of lymph fluid")
    HYDROCELE = ("A hydrocele is a buildup of fluid in the scrotum, the pouch of skin that holds the testicles")

    DEFAULT_CONTENT = (
        "This impressive paella is a perfect party dish and a fun meal to cook "
        "together with your guests. Add 1 cup of frozen peas along with the mussels, "
        "if you like."
    )

    def __call__(self, content,disease,year,image):
        with mui.Card(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            mui.CardHeader(
                title=disease,
                subheader=year,
                # avatar=mui.Avatar("R", sx={"bgcolor": "red"}),
                action=mui.IconButton(mui.icon.MoreVert),
                className=self._draggable_class,
            )
           
            mui.CardMedia(
                    component="img",
                    height= 300,
                    image=image,
                    alt=disease,
                )
            
            with mui.CardContent(sx={"flex": 1}):
                mui.Typography(content)

            with mui.CardActions(disableSpacing=True):
                mui.IconButton(mui.icon.Favorite)
                mui.IconButton(mui.icon.Share)
