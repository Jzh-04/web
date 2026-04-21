from typing import List, Optional
from pydantic import BaseModel, Field


class PredictResponse(BaseModel):
    labels: List[str] = Field(default_factory=list, description="模型检测到的标签列表")
    top_label: Optional[str] = Field(default=None, description="置信度最高或首个标签")
    description: str = Field(..., description="基于标签生成的文本描述")
    image_url: Optional[str] = Field(default=None, description="检测结果图的访问路径")