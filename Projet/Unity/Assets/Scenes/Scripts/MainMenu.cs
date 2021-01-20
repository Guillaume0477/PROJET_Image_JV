using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class MainMenu : MonoBehaviour
{
    public string sceneToLoad;
    public string sceneToLoad2;
    public RectTransform settings;

    public void StartGame()
    {
        SceneManager.LoadScene(sceneToLoad);
        Time.timeScale = 1;
    }

    public void Tutorial()
    {
        SceneManager.LoadScene(sceneToLoad2);
    }

    public void Settings()
    {
        settings.gameObject.SetActive(true);
    }

    public void QuitGame()
    {
        Application.Quit();
    }
}
