# external import
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates


# insernal import
from routers.roomBookingRoutes import get_All_Rooms

templateRoutes = APIRouter()
templates = Jinja2Templates(directory="templates")


@templateRoutes.get("/")
async def home_page(req: Request, response_class=HTMLResponse):

    try:
        user_info = req.state.user_info

        if len(user_info) == 0:
            return RedirectResponse("/login")

    except:
        return RedirectResponse("/login")

    all_rooms = await get_All_Rooms()
    print(all_rooms)
    return templates.TemplateResponse(
        request=req,
        name="home.html",
        context={"user_info": user_info, "all_rooms": all_rooms},
    )


@templateRoutes.get("/add")
async def add_page(req: Request):

    try:
        user_info = req.state.user_info

        if len(user_info) == 0:
            return RedirectResponse("/login")

    except:
        return RedirectResponse("/login")

    return templates.TemplateResponse(
        request=req, name="add.html", context={"user_info": user_info}
    )


@templateRoutes.get("/booking")
async def add_page(req: Request, from_date: str | None  = None, to_date: str|None = None):

    print("booking/search")
    try:
        user_info = req.state.user_info

        if len(user_info) == 0:
            return RedirectResponse("/login")

    except:
        return RedirectResponse("/login")

    print(from_date, to_date)

    return templates.TemplateResponse(
        request=req, name="booking.html", context={"user_info": user_info}
    )




@templateRoutes.get("/login")
async def login_page(req: Request, response_class=HTMLResponse):
    return templates.TemplateResponse(request=req, name="login.html")


@templateRoutes.get("/signup")
async def login_page(req: Request, response_class=HTMLResponse):
    return templates.TemplateResponse(request=req, name="signup.html")
