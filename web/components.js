const header = `

`


const second_screen = `
		<div class='content-wrapper'>
            <img 
            	class='video-box'
            	alt="Stream"
            	src=""
            	id="video-box"
            	data-src="loading.png"
            />
        </div>
		`

// function selectFile() {
// 	const fileInput = document.getElementById('fileInput');
// 	fileInput.click();
// }

function uploadFile(input) {
    const selectedFile = input.files[0];
    if (selectedFile) {
        // Здесь можно добавить код для загрузки или обработки файла
        console.log(`Выбран файл: ${selectedFile.name}`);
    }
}


const main_screen = `
<div class='start-wrapper'>
            <div class='title'>
                Начать работу
            </div>
            <div class='description'>
                Выберите источник для анализа.
            </div>
            <div
                    class='main-button'
                    id="open-camera"
            >
                <div class='text-button'>
                    Обзор с камер
                </div>
            </div>
            
            <input type="file" id="fileInput" style="display: none;">
            
            <div class='field' id="file-field">
                <div class='text-title-field'>
                    Добавьте файл или перетащите его в это окно
                </div>
                <div class="text-desc-field" id="field-format">
                    Поддерживаемые форматы: mp4, jpeg
                </div>
            </div>
            
        </div>
        <div class='add-wrapper'>
            <div class='settings-wrapper'>
                <div class='title'>
                    Параметры
                </div>
                <div class='object-wrapper-settings'>
                    <div class='text-wrapper-settings'>
                        <div class='title-settings'>
                            Объект
                        </div>
                    </div>
                    <div class='params-wrapper'>
                        <div class='params-item'>
                            <div class='param-title'>
                                Размер шрифта
                            </div>
                            <div class='counter'>
                                <div class="count-button">
                                    <svg class='count-icon' xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                         viewBox="0 0 16 16" fill="none">
                                        <rect width="16" height="16" rx="8"/>
                                        <rect x="4" y="7" width="8" height="2" rx="1" fill="#D9D9D9"/>
                                    </svg>
                                </div>
                                <div class='text-count'>
                                    12
                                </div>
                                <div class="count-button">
                                    <svg class='count-icon' xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                         viewBox="0 0 16 16" fill="none">
                                        <rect width="16" height="16" rx="8"/>
                                        <rect x="9.00018" y="4.00005" width="8" height="2" rx="1"
                                              transform="rotate(90 9.00018 4.00005)"
                                              fill="#D9D9D9"/>
                                        <rect x="4" y="7" width="8" height="2" rx="1" fill="#D9D9D9"/>
                                    </svg>
                                </div>
                            </div>
                        </div>
                        <div class='breaker'></div>
                        <div class='params-item'>
                            <div class='param-title'>
                                Цвет рамки
                            </div>
                            <div class='color-picker'>
                            </div>
                        </div>
                    </div>
                </div>
                
                                <div class='object-wrapper-settings'>
                    <div class='text-wrapper-settings'>
                        <div class='title-settings'>
                            Режим обработки
                        </div>
                    </div>
                    <div class='button-select-wrapper'>
                        <div class='button-select' id="analysis">
                           Анализ
                        </div>
                         <div class='button-select' id="pre_training">
                           Дообучение
                        </div>
                    </div>
                     <div class='text-wrapper-settings'>
                        <div class='desc-settings' id="desc-settings">
                           Описание
                        </div>
                    </div>
                    
                    
                </div>
            </div>
            <div
                    class='info-wrapper'>
                <img class='hack-logo'
                     src="./img/83584adf015b35772b15e04232bad07a.png"/>
            </div>
        </div>
    </div>
`


const play_second_screen = `
<div class='pause-button'>
                    <svg class='pause-icon' xmlns="http://www.w3.org/2000/svg" width="8" height="12" viewBox="0 0 8 12" fill="none">
                        <path fill-rule="evenodd" clip-rule="evenodd"
                            d="M1 0C0.447715 0 0 0.447715 0 1V11C0 11.5523 0.447715 12 1 12C1.55229 12 2 11.5523 2 11V1C2 0.447715 1.55229 0 1 0ZM7 0C6.44771 0 6 0.447715 6 1V11C6 11.5523 6.44771 12 7 12C7.55228 12 8 11.5523 8 11V1C8 0.447715 7.55228 0 7 0Z"
                            fill="#D9D9D9" />
                    </svg>
                </div>
`

const play_main_screen = `
	<div class='play-button'>
	<svg class='play-icon' xmlns="http://www.w3.org/2000/svg" width="10" height="12" viewBox="0 0 10 12"
	fill="none">
	<path
	d="M9.5 5.13397C10.1667 5.51887 10.1667 6.48113 9.5 6.86603L2 11.1962C1.33333 11.5811 0.5 11.0999 0.5 10.3301L0.5 1.66987C0.5 0.900073 1.33333 0.418947 2 0.803848L9.5 5.13397Z"
	fill="#D9D9D9"/>
	</svg>
	</div>
`