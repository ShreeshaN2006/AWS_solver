from bs4 import BeautifulSoup

from app.models.schemas import CourseOutlineItem


class CanvasParserService:
    def parse_modules(self, html: str) -> list[CourseOutlineItem]:
        soup = BeautifulSoup(html, "html.parser")
        modules: list[CourseOutlineItem] = []
        for module in soup.select(".context_module"):
            module_id = module.get("id", "unknown").replace("context_module_", "")
            title_node = module.select_one(".name")
            module_title = title_node.get_text(strip=True) if title_node else "Untitled Module"
            for item in module.select(".items .context_module_item"):
                item_title = item.get_text(" ", strip=True)
                anchor = item.select_one("a")
                modules.append(
                    CourseOutlineItem(
                        module_id=module_id,
                        module_title=module_title,
                        item_title=item_title,
                        item_link=anchor.get("href") if anchor else None,
                    )
                )
        return modules


canvas_parser = CanvasParserService()
