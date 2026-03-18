from selenium.webdriver.remote.webdriver import WebDriver as Remote
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
import os
import time
import traceback

# 尝试导入python-dotenv，如果未安装则提示
try:
    from dotenv import load_dotenv
    load_dotenv()  # 加载.env文件中的环境变量
    DOTENV_AVAILABLE = True
except ImportError:
    print("警告: 未安装python-dotenv库，将使用默认配置")
    print("请安装: pip install python-dotenv")
    DOTENV_AVAILABLE = False

# ========== 配置部分 ==========
# 从环境变量或默认值获取配置
if DOTENV_AVAILABLE:
    MOBILE_NUMBER = os.getenv('YUKETANG_USERNAME', '您的手机号')
    PASSWORD = os.getenv('YUKETANG_PASSWORD', '您的密码')
else:
    MOBILE_NUMBER = "您的手机号"
    PASSWORD = "您的密码"

COURSE_NAME = "创业:道与术(创新创业基础)"  # 要选择的课程名称
# =============================

def main():
    driver = None
    try:
        chrome_options = Options()
        chrome_options.set_capability("browserName", "chrome")
        
        # 添加一些常用选项
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        print("正在连接到 Selenium Hub...")
        driver = Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            options=chrome_options
        )
        
        print("连接成功，正在访问雨课堂...")
        driver.get("https://www.yuketang.cn/web")
        
        # 等待页面加载完成
        wait = WebDriverWait(driver, 15)
        
        # 检查是否已经登录（跳转到首页）
        current_url = driver.current_url
        print(f"当前URL: {current_url}")
        
        if "www.yuketang.cn/v2/web/index" in current_url:
            print("已登录，跳过登录步骤")
        else:
            print("未登录，开始登录流程...")
            
            # 点击账号密码登录按钮
            try:
                # 首先尝试正常点击
                login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='账号密码登录']")))
                login_button.click()
                print("已点击账号密码登录按钮")
                time.sleep(2)
            except Exception as e:
                print(f"正常点击失败: {e}")
                print("尝试使用JavaScript点击...")
                try:
                    # 使用JavaScript直接点击元素，避免元素遮挡问题
                    login_button = driver.find_element(By.XPATH, "//img[@alt='账号密码登录']")
                    driver.execute_script("arguments[0].click();", login_button)
                    print("已使用JavaScript点击账号密码登录按钮")
                    time.sleep(2)
                except Exception as js_e:
                    print(f"JavaScript点击也失败: {js_e}")
                    print("尝试检查是否有服务器选择...")
                    
                    # 检查是否有服务器列表需要选择
                    try:
                        server_elements = driver.find_elements(By.XPATH, "//ul[@class='server-list']//li")
                        if server_elements:
                            print(f"找到 {len(server_elements)} 个服务器选项")
                            # 尝试点击第一个服务器
                            server_elements[0].click()
                            print("已选择第一个服务器")
                            time.sleep(2)
                            
                            # 再次尝试点击登录按钮
                            login_button = driver.find_element(By.XPATH, "//img[@alt='账号密码登录']")
                            driver.execute_script("arguments[0].click();", login_button)
                            print("已点击账号密码登录按钮")
                            time.sleep(2)
                    except Exception as server_e:
                        print(f"处理服务器选择失败: {server_e}")
                        print("尝试直接查找登录表单输入框...")
            
            # 输入手机号
            try:
                mobile_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='mobile' and @name='loginname']")))
                mobile_input.clear()
                mobile_input.send_keys(MOBILE_NUMBER)
                print(f"已输入手机号: {MOBILE_NUMBER}")
                time.sleep(1)
            except TimeoutException:
                print("错误: 未找到手机号输入框")
                raise
            
            # 输入密码
            try:
                password_input = driver.find_element(By.XPATH, "//input[@type='password' and @name='password']")
                password_input.clear()
                password_input.send_keys(PASSWORD)
                print(f"已输入密码 (长度: {len(PASSWORD)})")
                time.sleep(1)
            except NoSuchElementException:
                print("错误: 未找到密码输入框")
                raise
            
            # 点击登录按钮
            try:
                submit_button = driver.find_element(By.XPATH, "//div[contains(@class, 'submit-btn') and contains(@class, 'login-btn') and text()='登录']")
                submit_button.click()
                print("已点击登录按钮")
                time.sleep(3)
            except NoSuchElementException:
                print("错误: 未找到登录按钮")
                raise
            
            # 等待登录成功跳转
            try:
                # 等待最多10秒，检查是否跳转到首页
                wait.until(EC.url_contains("www.yuketang.cn/v2/web/index"))
                print("登录成功，已跳转到首页")
            except TimeoutException:
                print("警告: 登录后未跳转到预期页面")
                print(f"当前URL: {driver.current_url}")
                
                # 检查是否有错误提示
                try:
                    error_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'error') or contains(@class, 'message')]")
                    for error in error_elements:
                        if error.text.strip():
                            print(f"页面错误提示: {error.text.strip()}")
                except:
                    pass
                
                # 检查页面标题和内容
                print(f"页面标题: {driver.title}")
                
                # 尝试截屏以便调试
                try:
                    driver.save_screenshot("login_debug.png")
                    print("已保存登录页面截图: login_debug.png")
                except:
                    print("无法保存截图")
                
                print("\n登录失败，停止执行后续操作")
                print("请检查用户名和密码是否正确，或查看login_debug.png截图")
                return  # 直接返回，不执行后续操作
        
        # 点击"我听的课"标签
        try:
            student_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='tab-student' and contains(@class, 'el-tabs__item') and text()='我听的课']")))
            student_tab.click()
            print("已点击'我听的课'标签")
            time.sleep(3)
        except TimeoutException:
            print("错误: 未找到'我听的课'标签")
            # 尝试其他方式查找
            try:
                tabs = driver.find_elements(By.XPATH, "//div[contains(@class, 'el-tabs__item')]")
                for tab in tabs:
                    if "我听的课" in tab.text:
                        tab.click()
                        print("已通过文本匹配点击'我听的课'标签")
                        time.sleep(3)
                        break
            except Exception as e:
                print(f"尝试其他方式查找标签失败: {e}")
                raise
        
        # 查找并点击指定课程（通过课程名称匹配）
        course_name = COURSE_NAME
        try:
            # 查找包含课程名称的元素
            course_elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{course_name}')]")
            
            if course_elements:
                course_found = False
                # 找到最外层的课程卡片元素
                for element in course_elements:
                    # 向上查找课程卡片容器
                    parent = element
                    for _ in range(5):  # 最多向上查找5层
                        parent = parent.find_element(By.XPATH, "./..")
                        class_attr = parent.get_attribute("class")
                        if class_attr and ("lesson-cardS" in class_attr or "studentCol" in class_attr):
                            parent.click()
                            print(f"已点击课程: {course_name}")
                            time.sleep(3)
                            course_found = True
                            break
                    if course_found:
                        break
                
                if not course_found:
                    print(f"警告: 找到课程文本但未找到可点击的卡片")
                    # 尝试直接点击第一个找到的元素
                    course_elements[0].click()
                    print(f"已直接点击课程文本: {course_name}")
                    time.sleep(3)
            else:
                print(f"错误: 未找到课程: {course_name}")
                # 列出所有可见的课程
                print("当前页面可见的课程:")
                all_texts = driver.find_elements(By.XPATH, "//h1 | //div[contains(@class, 'lesson-cardS')]//h1")
                for text_elem in all_texts:
                    if text_elem.text.strip():
                        print(f"  - {text_elem.text.strip()}")
                raise NoSuchElementException(f"课程 '{course_name}' 未找到")
        except Exception as e:
            print(f"选择课程时出错: {e}")
            traceback.print_exc()
            raise
        
        # 点击"学习内容"标签
        try:
            content_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='tab-content' and contains(@class, 'el-tabs__item') and text()='学习内容']")))
            content_tab.click()
            print("已点击'学习内容'标签")
            time.sleep(3)
        except TimeoutException:
            print("错误: 未找到'学习内容'标签")
            # 尝试其他方式查找
            try:
                tabs = driver.find_elements(By.XPATH, "//div[contains(@class, 'el-tabs__item') and contains(text(), '学习内容')]")
                if tabs:
                    tabs[0].click()
                    print("已通过文本匹配点击'学习内容'标签")
                    time.sleep(3)
                else:
                    print("未找到任何包含'学习内容'文本的标签")
            except Exception as e:
                print(f"尝试其他方式查找学习内容标签失败: {e}")
        
        # 主循环：处理所有未完成章节
        max_chapters_to_process = 20  # 最多处理20个章节，防止无限循环
        chapters_processed = 0
        
        while chapters_processed < max_chapters_to_process:
            print(f"\n{'='*60}")
            print(f"开始查找未完成的章节 (第 {chapters_processed + 1} 轮)...")
            print(f"{'='*60}")
            
            # 等待页面稳定
            time.sleep(3)
            
            # 首先尝试切换到iframe内部查找章节项
            chapter_items = []
            in_iframe = False
            
            try:
                # 查找iframe元素
                iframe_elements = driver.find_elements(By.XPATH, "//iframe[contains(@class, 'tab-pane-content-iframe')]")
                
                if iframe_elements:
                    iframe = iframe_elements[0]
                    print("找到iframe，正在切换到iframe上下文...")
                    driver.switch_to.frame(iframe)
                    in_iframe = True
                    
                    # 在iframe内部查找章节项
                    chapter_items = driver.find_elements(By.XPATH, "//div[contains(@class, 'el-tooltip') and contains(@class, 'leaf-detail')]")
                    print(f"在iframe内部找到 {len(chapter_items)} 个章节项")
                else:
                    print("未找到iframe元素，尝试在主文档中查找...")
                    chapter_items = driver.find_elements(By.XPATH, "//div[contains(@class, 'el-tooltip') and contains(@class, 'leaf-detail')]")
            except Exception as e:
                print(f"切换到iframe时出错: {e}")
                # 出错时确保在主文档
                try:
                    driver.switch_to.default_content()
                    in_iframe = False
                except:
                    pass
                chapter_items = driver.find_elements(By.XPATH, "//div[contains(@class, 'el-tooltip') and contains(@class, 'leaf-detail')]")
            
            if not chapter_items:
                print("未找到章节项，尝试刷新页面并重新点击学习内容标签...")
                driver.refresh()
                time.sleep(5)
                
                # 刷新后重新点击学习内容标签
                try:
                    content_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='tab-content' and contains(@class, 'el-tabs__item') and text()='学习内容']")))
                    content_tab.click()
                    print("已重新点击'学习内容'标签")
                    time.sleep(3)
                except TimeoutException:
                    print("错误: 刷新后未找到'学习内容'标签")
                    # 尝试其他方式查找
                    try:
                        tabs = driver.find_elements(By.XPATH, "//div[contains(@class, 'el-tabs__item') and contains(text(), '学习内容')]")
                        if tabs:
                            tabs[0].click()
                            print("已通过文本匹配重新点击'学习内容'标签")
                            time.sleep(3)
                        else:
                            print("未找到任何包含'学习内容'文本的标签")
                    except Exception as e:
                        print(f"尝试重新点击学习内容标签失败: {e}")
                
                # 再次尝试查找章节项
                try:
                    # 切换到iframe
                    iframe_elements = driver.find_elements(By.XPATH, "//iframe[contains(@class, 'tab-pane-content-iframe')]")
                    if iframe_elements:
                        iframe = iframe_elements[0]
                        driver.switch_to.frame(iframe)
                        in_iframe = True
                        chapter_items = driver.find_elements(By.XPATH, "//div[contains(@class, 'el-tooltip') and contains(@class, 'leaf-detail')]")
                        print(f"刷新后在iframe内部找到 {len(chapter_items)} 个章节项")
                except Exception as e:
                    print(f"刷新后查找章节项时出错: {e}")
                    try:
                        driver.switch_to.default_content()
                        in_iframe = False
                    except:
                        pass
            
            if chapter_items:
                print(f"找到 {len(chapter_items)} 个章节项")
                
                # 查找第一个未完成的章节
                unfinished_item = None
                unfinished_title = ""
                unfinished_reason = ""
                
                for i, item in enumerate(chapter_items):
                    try:
                        # 获取章节标题
                        title_element = item.find_element(By.XPATH, ".//span[contains(@class, 'title')]")
                        title = title_element.text.strip()
                        
                        # 获取进度状态
                        progress_element = item.find_element(By.XPATH, ".//div[contains(@class, 'progress-wrap')]")
                        progress_text = progress_element.text.strip()
                        
                        print(f"\n章节 {i+1}: {title}")
                        print(f"进度状态: {progress_text}")
                        
                        # 判断是否未完成
                        is_unfinished = False
                        reason = ""
                        
                        if "未开始" in progress_text:
                            is_unfinished = True
                            reason = "未开始"
                        elif "未发言" in progress_text:
                            is_unfinished = True
                            reason = "未发言"
                        elif "%" in progress_text:
                            # 提取百分比数字
                            import re
                            percent_match = re.search(r'(\d+)%', progress_text)
                            if percent_match:
                                percent = int(percent_match.group(1))
                                if percent < 100:
                                    is_unfinished = True
                                    reason = f"进度{percent}%"
                        elif "已完成" not in progress_text and progress_text:
                            is_unfinished = True
                            reason = f"其他状态: {progress_text}"
                        
                        if is_unfinished:
                            print(f"✓ 发现未完成章节: {title} ({reason})")
                            if unfinished_item is None:
                                unfinished_item = item
                                unfinished_title = title
                                unfinished_reason = reason
                                break
                        else:
                            print(f"  ✓ 已完成: {title}")
                            
                    except Exception as item_e:
                        print(f"处理章节 {i+1} 时出错: {item_e}")
                        continue
                
                # 处理完章节项后，如果需要切换回主文档
                if in_iframe and unfinished_item is None:
                    # 如果没有找到未完成章节，切换回主文档
                    try:
                        driver.switch_to.default_content()
                        in_iframe = False
                        print("未找到未完成章节，已切换回主文档")
                    except Exception as switch_e:
                        print(f"切换回主文档时出错: {switch_e}")
                
                if unfinished_item:
                    print(f"\n=== 找到未完成章节 ===")
                    print(f"章节标题: {unfinished_title}")
                    print(f"未完成原因: {unfinished_reason}")
                    
                    # 尝试点击该章节
                    try:
                        print("正在点击章节...")
                        
                        # 如果我们在iframe内部找到的章节项，确保在iframe内部点击
                        if in_iframe:
                            print("在iframe内部点击章节项")
                        else:
                            # 如果不在iframe内部，尝试切换到iframe
                            try:
                                iframe_elements = driver.find_elements(By.XPATH, "//iframe[contains(@class, 'tab-pane-content-iframe')]")
                                if iframe_elements:
                                    iframe = iframe_elements[0]
                                    driver.switch_to.frame(iframe)
                                    in_iframe = True
                                    print("已切换到iframe内部点击章节")
                            except Exception as iframe_e:
                                print(f"切换到iframe时出错: {iframe_e}")
                        
                        # 先尝试正常点击
                        try:
                            unfinished_item.click()
                            print("已正常点击章节")
                        except Exception as click_e:
                            print(f"正常点击失败: {click_e}")
                            print("尝试使用JavaScript点击...")
                            
                            # 使用JavaScript点击
                            driver.execute_script("arguments[0].click();", unfinished_item)
                            print("已使用JavaScript点击章节")
                        
                        # 等待页面响应
                        time.sleep(3)
                        
                        # 检查是否跳转或加载了新内容
                        print(f"点击后URL: {driver.current_url}")
                        print(f"点击后页面标题: {driver.title}")
                        
                        # 尝试截屏记录
                        try:
                            driver.save_screenshot(f"chapter_{chapters_processed + 1}_clicked.png")
                            print(f"已保存点击后截图: chapter_{chapters_processed + 1}_clicked.png")
                        except:
                            pass
                        
                        # 视频播放和进度监控
                        print("\n=== 开始视频播放和进度监控 ===")
                        
                        # 确保在iframe内部
                        try:
                            # 检查是否已经在iframe内部，如果没有则切换到iframe
                            current_frame = driver.execute_script("return window.frameElement;")
                            if not current_frame:
                                iframe_elements = driver.find_elements(By.XPATH, "//iframe[contains(@class, 'tab-pane-content-iframe')]")
                                if iframe_elements:
                                    iframe = iframe_elements[0]
                                    driver.switch_to.frame(iframe)
                                    print("已切换到iframe内部进行视频播放")
                        except Exception as iframe_check_e:
                            print(f"检查iframe状态时出错: {iframe_check_e}")
                        
                        # 等待DOM加载完成
                        print("等待DOM加载完成...")
                        time.sleep(5)
                        
                        # 查找并点击播放按钮
                        play_button_clicked = False
                        try:
                            # 使用更通用的播放按钮选择器列表，按优先级排序
                            play_button_selectors = [
                                "//button[contains(@class, 'play')]",  # 最通用的选择器
                                "//button[contains(@class, 'xt_video_bit_play_btn') and contains(@class, 'blue_play_btn')]",
                                "//div[contains(@class, 'play-btn')]",
                                "//*[contains(text(), '播放')]",
                                "//button[contains(@class, 'video-play')]",
                                "//button[contains(@class, 'play-button')]",
                                "//div[contains(@class, 'play-button')]",
                                "//button[@title='播放']",
                                "//button[@aria-label='播放']"
                            ]
                            
                            play_buttons = None
                            selected_selector = None
                            
                            for selector in play_button_selectors:
                                try:
                                    buttons = driver.find_elements(By.XPATH, selector)
                                    if buttons:
                                        play_buttons = buttons
                                        selected_selector = selector
                                        print(f"使用选择器 '{selector}' 找到 {len(buttons)} 个播放相关按钮")
                                        break
                                except:
                                    pass
                            
                            if play_buttons:
                                # 尝试点击第一个播放按钮
                                try:
                                    play_buttons[0].click()
                                    print(f"已点击播放按钮 (使用选择器: {selected_selector})")
                                    play_button_clicked = True
                                except Exception as play_click_e:
                                    print(f"正常点击播放按钮失败: {play_click_e}")
                                    print("尝试使用JavaScript点击播放按钮...")
                                    driver.execute_script("arguments[0].click();", play_buttons[0])
                                    print(f"已使用JavaScript点击播放按钮 (使用选择器: {selected_selector})")
                                    play_button_clicked = True
                            else:
                                print("未找到任何播放按钮，尝试其他方法...")
                                
                                # 尝试查找视频元素并直接播放
                                try:
                                    video_elements = driver.find_elements(By.TAG_NAME, "video")
                                    if video_elements:
                                        print(f"找到 {len(video_elements)} 个视频元素，尝试直接播放")
                                        driver.execute_script("arguments[0].play();", video_elements[0])
                                        print("已尝试直接播放视频")
                                        play_button_clicked = True
                                except Exception as video_e:
                                    print(f"尝试直接播放视频失败: {video_e}")
                        except Exception as play_error:
                            print(f"查找播放按钮时出错: {play_error}")
                        
                        progress_completed = False  # 初始化变量
                        
                        if play_button_clicked:
                            print("播放按钮已点击，开始监控进度...")
                            
                            # 监控进度条，等待完成度达到100%
                            max_wait_time = 3600  # 最大等待30分钟
                            check_interval = 30    # 每30秒检查一次
                            total_wait_time = 0
                            progress_completed = False
                            
                            while total_wait_time < max_wait_time and not progress_completed:
                                try:
                                    # 查找进度条元素
                                    progress_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'el-tooltip') and contains(@class, 'item')]//span[contains(text(), '完成度：')]")
                                    
                                    if progress_elements:
                                        progress_text = progress_elements[0].text.strip()
                                        print(f"进度状态: {progress_text}")
                                        
                                        # 提取百分比或检查是否已完成
                                        import re
                                        percent_match = re.search(r'(\d+)%', progress_text)
                                        
                                        if percent_match:
                                            percent = int(percent_match.group(1))
                                            # print(f"当前完成度: {percent}%")
                                            
                                            if percent >= 100:
                                                print("✓ 视频已完成！")
                                                progress_completed = True
                                                break
                                        elif "已完成" in progress_text:
                                            print("✓ 视频已完成！(状态显示为'已完成')")
                                            progress_completed = True
                                            break
                                        else:
                                            print("无法解析进度状态")
                                    else:
                                        print("未找到进度条元素，检查是否有完成提示元素...")
                                        
                                        # 当进度条元素消失时，检查是否有<span class="text">text</span>元素
                                        try:
                                            # 查找<span class="text">元素
                                            text_elements = driver.find_elements(By.XPATH, "//span[@class='text']")
                                            if text_elements:
                                                for elem in text_elements:
                                                    text_content = elem.text.strip()
                                                    if text_content:
                                                        print(f"找到text元素: {text_content[:50]}")
                                                        
                                                        # 检查是否包含完成相关的文本
                                                        if "完成" in text_content or "已观看" in text_content or "100%" in text_content:
                                                            print("✓ 视频已完成！(找到完成提示元素)")
                                                            progress_completed = True
                                                            break
                                                
                                                if progress_completed:
                                                    break
                                        except Exception as text_e:
                                            print(f"检查text元素时出错: {text_e}")
                                        
                                        # 尝试其他进度条选择器
                                        try:
                                            # 查找包含进度信息的元素
                                            progress_containers = driver.find_elements(By.XPATH, "//*[contains(text(), '完成') or contains(text(), '进度') or contains(text(), '%')]")
                                            for elem in progress_containers[:5]:
                                                text = elem.text.strip()
                                                if text:
                                                    print(f"可能的相关元素: {text[:50]}")
                                        except:
                                            pass
                                except Exception as progress_error:
                                    print(f"检查进度时出错: {progress_error}")
                                
                                # 等待一段时间再检查
                                # print(f"等待 {check_interval} 秒后再次检查... ({total_wait_time}/{max_wait_time}秒)")
                                time.sleep(check_interval)
                                total_wait_time += check_interval
                            
                            if progress_completed:
                                print("\n=== 视频学习完成 ===")
                                
                                # 返回课程选择页面
                                print("返回课程选择页面...")
                                try:
                                    # 首先切换回主文档
                                    try:
                                        driver.switch_to.default_content()
                                        print("已切换回主文档")
                                    except Exception as switch_e:
                                        print(f"切换回主文档时出错: {switch_e}")
                                    
                                    # 尝试点击返回按钮或后退
                                    back_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '返回') or contains(text(), 'Back') or contains(@class, 'back')]")
                                    if back_buttons:
                                        back_buttons[0].click()
                                        print("已点击返回按钮")
                                    else:
                                        # 使用浏览器后退
                                        driver.back()
                                        print("已使用浏览器后退")
                                    
                                    time.sleep(5)
                                    print(f"返回后URL: {driver.current_url}")
                                    
                                    # 返回后需要重新点击"学习内容"标签
                                    print("返回后重新点击'学习内容'标签...")
                                    try:
                                        content_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='tab-content' and contains(@class, 'el-tabs__item') and text()='学习内容']")))
                                        content_tab.click()
                                        print("已重新点击'学习内容'标签")
                                        time.sleep(3)
                                    except TimeoutException:
                                        print("错误: 返回后未找到'学习内容'标签")
                                        # 尝试其他方式查找
                                        try:
                                            tabs = driver.find_elements(By.XPATH, "//div[contains(@class, 'el-tabs__item') and contains(text(), '学习内容')]")
                                            if tabs:
                                                tabs[0].click()
                                                print("已通过文本匹配重新点击'学习内容'标签")
                                                time.sleep(3)
                                            else:
                                                print("未找到任何包含'学习内容'文本的标签")
                                        except Exception as e:
                                            print(f"尝试重新点击学习内容标签失败: {e}")
                                    
                                    # 增加已处理章节计数
                                    chapters_processed += 1
                                    print(f"已成功处理 {chapters_processed} 个章节")
                                    
                                    # 继续循环处理下一个章节
                                    continue
                                    
                                except Exception as back_error:
                                    print(f"返回时出错: {back_error}")
                                    # 即使返回失败，也增加计数并继续
                                    chapters_processed += 1
                                    continue
                            else:
                                print(f"\n警告: 在 {max_wait_time} 秒内未检测到视频完成")
                                print("可能原因: 1) 进度条元素未找到 2) 视频未正常播放 3) 页面结构不同")
                        else:
                            print("\n警告: 未能点击播放按钮，跳过视频播放")
                        
                        print("\n=== 视频处理完成 ===")
                        
                        # 如果视频处理完成但未达到100%，也增加计数
                        if not progress_completed:
                            chapters_processed += 1
                            print(f"视频未完成，但已尝试处理，计数增加到 {chapters_processed}")
                        
                    except Exception as click_error:
                        print(f"点击章节时出错: {click_error}")
                        traceback.print_exc()
                        # 即使出错也增加计数，避免卡在同一个章节
                        chapters_processed += 1
                        print(f"处理出错，计数增加到 {chapters_processed}")
                else:
                    print("\n=== 未找到未完成章节 ===")
                    print("所有章节似乎都已完成")
                    
                    # 列出所有章节状态供参考
                    print("\n所有章节状态:")
                    for i, item in enumerate(chapter_items[:10]):  # 只显示前10个
                        try:
                            title_element = item.find_element(By.XPATH, ".//span[contains(@class, 'title')]")
                            title = title_element.text.strip()[:50]  # 限制长度
                            progress_text = item.find_element(By.XPATH, ".//div[contains(@class, 'progress-wrap')]").text.strip()
                            print(f"  {i+1}. {title} - {progress_text}")
                        except:
                            pass
                    
                    # 所有章节都已完成，退出循环
                    print("\n✓ 所有章节已完成，停止处理")
                    break
            else:
                print("未找到章节项，尝试其他选择器...")
                
                # 尝试其他可能的选择器
                alternative_selectors = [
                    "//div[contains(@class, 'leaf-detail')]",
                    "//div[contains(@class, 'el-tooltip')]",
                    "//div[contains(@class, 'section-list')]//div[contains(@class, 'content')]//div",
                    "//*[contains(text(), '1.') or contains(text(), '2.') or contains(text(), '3.') or contains(text(), '4.')]"
                ]
                
                for selector in alternative_selectors:
                    try:
                        elements = driver.find_elements(By.XPATH, selector)
                        if elements:
                            print(f"使用选择器 '{selector}' 找到 {len(elements)} 个元素")
                            # 显示前几个元素的文本
                            for i, elem in enumerate(elements[:5]):
                                text = elem.text.strip()[:100]
                                if text:
                                    print(f"  元素 {i+1}: {text}")
                    except:
                        pass
                
                # 打印页面结构帮助调试
                print("\n当前页面body的前500个字符:")
                try:
                    body_html = driver.find_element(By.TAG_NAME, "body").get_attribute("outerHTML")
                    if body_html:
                        print(body_html[:500] + "...")
                    else:
                        print("body_html为None或空")
                except:
                    pass
                
                # 未找到章节项，增加计数并继续
                chapters_processed += 1
                print(f"未找到章节项，计数增加到 {chapters_processed}")
                
                # 尝试刷新页面
                try:
                    driver.refresh()
                    time.sleep(5)
                except:
                    pass
            
            # 检查是否达到最大处理次数
            if chapters_processed >= max_chapters_to_process:
                print(f"\n{'='*60}")
                print(f"已达到最大处理次数 ({max_chapters_to_process})，停止处理")
                print(f"{'='*60}")
                break
        
        print("\n=== 所有章节处理完成 ===")
        print(f"总共处理了 {chapters_processed} 个章节")
        
        print("\n操作完成，等待30秒以便观察...")
        time.sleep(30)
        
        print("测试完成，正在清理资源...")
    
    except WebDriverException as e:
        print(f"WebDriver 错误: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"其他错误: {e}")
        traceback.print_exc()
    finally:
        # 确保正确关闭 driver
        if driver:
            try:
                print("正在关闭浏览器会话...")
                driver.quit()  # 使用 quit() 而不是 close()
                print("浏览器会话已关闭")
            except Exception as e:
                print(f"关闭浏览器时出错: {e}")
        else:
            print("没有活动的浏览器会话需要关闭")

if __name__ == "__main__":
    main()
