using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class PauseMenu : MonoBehaviour
{
    public string sceneToLoad;
    public RectTransform menu;

    public void GoBackToGame()
    {
        menu.gameObject.SetActive(false);
        Time.timeScale = 1;
    }

    public void GoBackToMainMenu()
    {
        SceneManager.LoadScene(sceneToLoad);
    }

    public void QuitGame()
    {
        Application.Quit();
    }
}