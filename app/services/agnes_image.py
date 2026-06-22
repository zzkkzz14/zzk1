"""Agnes Image API 服务模块"""

import os
import requests
from typing import Optional, List, Dict


class AgnesImageService:
    """Agnes Image 2.1 Flash 图像生成服务"""
    
    BASE_URL = "https://apihub.agnes-ai.com/v1"
    MODEL_NAME = "agnes-image-2.1-flash"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("AGNES_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_image(self, 
                       prompt: str,
                       size: str = "1024x1024",
                       n: int = 1,
                       negative_prompt: Optional[str] = None) -> Dict:
        """
        文生图
        
        Args:
            prompt: 提示词
            size: 图像尺寸，支持 1024x1024, 2048x2048, 4096x4096 等
            n: 生成数量
            negative_prompt: 负面提示词
            
        Returns:
            生成结果
        """
        url = f"{self.BASE_URL}/images/generations"
        
        payload = {
            "model": self.MODEL_NAME,
            "prompt": prompt,
            "size": size,
            "n": n
        }
        
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def generate_image_from_image(self,
                                  image: str,
                                  prompt: str,
                                  size: str = "1024x1024",
                                  n: int = 1,
                                  strength: float = 0.7,
                                  negative_prompt: Optional[str] = None) -> Dict:
        """
        图生图
        
        Args:
            image: 输入图像（URL 或 base64 编码）
            prompt: 提示词
            size: 图像尺寸
            n: 生成数量
            strength: 变换强度 (0-1)
            negative_prompt: 负面提示词
            
        Returns:
            生成结果
        """
        url = f"{self.BASE_URL}/images/generations"
        
        payload = {
            "model": self.MODEL_NAME,
            "prompt": prompt,
            "size": size,
            "n": n,
            "image": image,
            "strength": strength
        }
        
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def get_supported_sizes(self) -> List[str]:
        """获取支持的图像尺寸"""
        return [
            "512x512",
            "1024x1024",
            "2048x2048",
            "4096x4096",
            "1024x768",
            "768x1024",
            "1920x1080",
            "1080x1920",
            "2560x1440",
            "1440x2560"
        ]
    
    def build_prompt(self, 
                     subject: str,
                     style: str = "",
                     details: str = "",
                     background: str = "",
                     lighting: str = "") -> str:
        """
        构建结构化提示词
        
        Args:
            subject: 主体描述
            style: 艺术风格
            details: 细节描述
            background: 背景描述
            lighting: 光照描述
            
        Returns:
            完整提示词
        """
        parts = [subject]
        if style:
            parts.append(f"in the style of {style}")
        if details:
            parts.append(details)
        if background:
            parts.append(f"background: {background}")
        if lighting:
            parts.append(f"lighting: {lighting}")
        
        return ", ".join(parts)


# 全局服务实例
agnes_service = AgnesImageService()