/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under Ultimate Liberty license
  * SLA0044, the "License"; You may not use this file except in compliance with
  * the License. You may obtain a copy of the License at:
  *                             www.st.com/SLA0044
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "usb_device.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "stdbool.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
#define Inductor1on HAL_GPIO_WritePin(Inductor1_GPIO_Port,Inductor1_Pin,1);
#define Inductor2on HAL_GPIO_WritePin(Inductor2_GPIO_Port,Inductor2_Pin,1);
#define Inductor3on HAL_GPIO_WritePin(Inductor3_GPIO_Port,Inductor3_Pin,1);
#define Inductor4on HAL_GPIO_WritePin(Inductor4_GPIO_Port,Inductor4_Pin,1);
#define Inductor5on HAL_GPIO_WritePin(Inductor5_GPIO_Port,Inductor5_Pin,1);
#define Inductor6on HAL_GPIO_WritePin(Inductor6_GPIO_Port,Inductor6_Pin,1);
#define Inductor7on HAL_GPIO_WritePin(Inductor7_GPIO_Port,Inductor7_Pin,1);

#define Inductor1off HAL_GPIO_WritePin(Inductor1_GPIO_Port,Inductor1_Pin,0);
#define Inductor2off HAL_GPIO_WritePin(Inductor2_GPIO_Port,Inductor2_Pin,0);
#define Inductor3off HAL_GPIO_WritePin(Inductor3_GPIO_Port,Inductor3_Pin,0);
#define Inductor4off HAL_GPIO_WritePin(Inductor4_GPIO_Port,Inductor4_Pin,0);
#define Inductor5off HAL_GPIO_WritePin(Inductor5_GPIO_Port,Inductor5_Pin,0);
#define Inductor6off HAL_GPIO_WritePin(Inductor6_GPIO_Port,Inductor6_Pin,0);
#define Inductor7off HAL_GPIO_WritePin(Inductor7_GPIO_Port,Inductor7_Pin,0);

#define ConcatCommand(a,b,c) a##b##c

#define TurnOnInductor(a,b) if(b==1) {ConcatCommand(Inductor,1,on);} \
else if(b==2){ConcatCommand(Inductor,2,on);} \
else if(b==3){ConcatCommand(Inductor,3,on);} \
else if(b==4){ConcatCommand(Inductor,4,on);} \
else if(b==5){ConcatCommand(Inductor,5,on);} \
else if(b==6){ConcatCommand(Inductor,6,on);} \
else if(b==7){ConcatCommand(Inductor,7,on);} \

#define TurnOffInductor(a,b) if(b==1) {ConcatCommand(Inductor,1,off);} \
else if(b==2){ConcatCommand(Inductor,2,off);} \
else if(b==3){ConcatCommand(Inductor,3,off);} \
else if(b==4){ConcatCommand(Inductor,4,off);} \
else if(b==5){ConcatCommand(Inductor,5,off);} \
else if(b==6){ConcatCommand(Inductor,6,off);} \
else if(b==7){ConcatCommand(Inductor,7,off);} \

int commandMode = 0 ;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */
int _write(int fd, char *ptr, int len) {
	CDC_Transmit_FS((uint8_t*) ptr, len);
	return len;
}

int ToInt(char c);
int CheckTypeOfCommand(char command[]);
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USB_DEVICE_Init();
  /* USER CODE BEGIN 2 */
  for(int i=1;i<8;i++)
  	  TurnOffInductor(Inductor,i);

  HAL_GPIO_WritePin(LED1_GPIO_Port,LED1_Pin,1);
  HAL_GPIO_WritePin(LED2_GPIO_Port,LED2_Pin,1);
  HAL_GPIO_WritePin(LED3_GPIO_Port,LED3_Pin,0);
  HAL_Delay(1000);
  HAL_GPIO_WritePin(LED1_GPIO_Port,LED1_Pin,0);
  HAL_GPIO_WritePin(LED2_GPIO_Port,LED2_Pin,0);
  HAL_GPIO_WritePin(LED3_GPIO_Port,LED3_Pin,1);
  HAL_Delay(1000);
  HAL_GPIO_WritePin(LED1_GPIO_Port,LED1_Pin,1);
  HAL_GPIO_WritePin(LED2_GPIO_Port,LED2_Pin,1);
  HAL_GPIO_WritePin(LED3_GPIO_Port,LED3_Pin,0);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV1;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USB;
  PeriphClkInit.UsbClockSelection = RCC_USBCLKSOURCE_PLL_DIV1_5;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */
void CDC_RecieveCallBack(uint8_t* Buf, uint32_t len) {

	char command[30]={'\0'};
	strncpy(command,Buf,len);
	CDC_Transmit_FS(command, strlen(command));

	if (CheckTypeOfCommand(command) == 1){
		HAL_GPIO_WritePin(LED2_GPIO_Port,LED2_Pin,0);
		TurnOnInductor(Inductor,ToInt(command[strlen("Inductor")]));
		HAL_GPIO_TogglePin(LED1_GPIO_Port,LED1_Pin);
	}else if(commandMode == 2){
		HAL_GPIO_WritePin(LED1_GPIO_Port,LED1_Pin,0);
		TurnOffInductor(Inductor,ToInt(command[strlen("Inductor")]));
		HAL_GPIO_TogglePin(LED2_GPIO_Port,LED2_Pin);
	}else if(commandMode == 3){
		HAL_GPIO_WritePin(LED1_GPIO_Port,LED1_Pin,0);
		HAL_GPIO_WritePin(LED2_GPIO_Port,LED2_Pin,0);
//		for (int i=1;i<8;i++)
//			TurnOffInductor(Inductor,i);
		for(int i=0;i<strlen(command);i++){
			if(isdigit(command[i])){
				TurnOnInductor(Inductor,ToInt(command[i]));
				HAL_GPIO_WritePin(LED1_GPIO_Port,LED1_Pin,1);
				HAL_GPIO_WritePin(LED2_GPIO_Port,LED2_Pin,1);
			}else break;
		}
	}else if(commandMode == 4){
		HAL_GPIO_WritePin(LED1_GPIO_Port,LED1_Pin,1);
		HAL_GPIO_WritePin(LED2_GPIO_Port,LED2_Pin,1);
//		for (int i=1;i<8;i++)
//			TurnOffInductor(Inductor,i);
		for(int i=0;i<strlen(command);i++){
			if(isdigit(command[i])){
				TurnOffInductor(Inductor,ToInt(command[i]));
				HAL_GPIO_WritePin(LED1_GPIO_Port,LED1_Pin,0);
				HAL_GPIO_WritePin(LED2_GPIO_Port,LED2_Pin,0);
			}else break;
		}



}
}


int CheckTypeOfCommand(char command[]){

	HAL_GPIO_WritePin(LED1_GPIO_Port,LED1_Pin,0);
	HAL_GPIO_WritePin(LED2_GPIO_Port,LED2_Pin,0);
	if(command[strlen(command)-1]=='n'){
		commandMode = 1;
	}else if(command[strlen(command)-1]=='f'){
		commandMode =2;
	}else if(command[strlen(command)-1]=='X'){
		commandMode =3;
	}else if(command[strlen(command)-1]=='Z'){
		commandMode=4;
	}

	return commandMode;

}

int ToInt(char c){
	return c - '0';
}
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
