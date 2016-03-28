package com.example.tests;
import org.apache.jasper.tagplugins.jstl.core.Catch;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.remote.CapabilityType;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.support.ui.Select;

import java.lang.*;

import java.util.Collection;
import java.util.concurrent.TimeUnit;
import java.awt.*;
import java.awt.event.KeyEvent;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;

public class Emedical_Main_Class {

    private boolean acceptNextAlert = true;
    private WebDriver driver;
    private String baseUrl = "http://ehealth.3continents.pro/";
    private StringBuffer verificationErrors = new StringBuffer();
    int a;
    int i;
    //int pageUP;
    int tablelanenumber =1;
    int calendarday = 1;
    String descriptionText;
    String Nodescriptiontext;
    String Password = "zaq123";
    int emailnumber =1;
    int appointmentcount = 1;

    @Before
    public void setUp() throws Exception
    {
/*
        String PROXY = "mg-pr-it1.memeglobal.com:3128";
        org.openqa.selenium.Proxy proxy = new org.openqa.selenium.Proxy();
        proxy.setHttpProxy(PROXY)
                .setFtpProxy(PROXY)
                .setSslProxy(PROXY);
        DesiredCapabilities cap = new DesiredCapabilities();
        cap.setCapability(CapabilityType.PROXY, proxy);
        driver = new FirefoxDriver(cap);*/
        driver = new FirefoxDriver();


        driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
        driver.manage().timeouts().setScriptTimeout(30, TimeUnit.SECONDS);
        driver.manage().timeouts().pageLoadTimeout(30,TimeUnit.SECONDS);

}

        @Test
    public void testUntitled() throws Exception {



            //region CREATE SOME APPOINTMENTS FROM PATIENTS INCLUCING PAYMENT METHOD
//~~~~~~~~~~~~~~~~~~CREATE SOME APPOINTMENTS FROM PATIENTS INCLUCING PAYMENT METHOD
            for(appointmentcount = 1; appointmentcount < 10;appointmentcount++) {
                for (emailnumber = 2; emailnumber < 9; emailnumber++) {
                    driver.manage().timeouts().implicitlyWait(15, TimeUnit.SECONDS);
                    driver.get(baseUrl + "en/");
                    driver.findElement(By.partialLinkText("LOGIN")).click();
                    driver.findElement(By.id("id_login")).clear();
                    driver.findElement(By.id("id_login")).sendKeys("emedicaltest" + emailnumber + "@gmail.com");
                    driver.findElement(By.id("id_password")).clear();
                    driver.findElement(By.id("id_password")).sendKeys(Password);
                    driver.findElement(By.xpath("//button[@type='submit']")).click();

                    driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[2]/div/ul/li[2]/a")).click();
                    driver.findElement(By.partialLinkText("AZCONA GUERRA")).click();

                    try {
                        isElementPresent(By.cssSelector("button.btn-u.show-schedule"));
                    } catch (Exception e) {
                    }
                    Thread.sleep(2000);
                    driver.findElement(By.cssSelector("button.btn-u.show-schedule")).click();
                    Thread.sleep(4000);

                    driver.findElement(By.cssSelector("html body.modal-open div.wrapper div div.container.content.profile div.row div.talk-to-doctor-container div#cur-doctor.modal.fade.in div.modal-dialog.modal-lg.doctor-info div.modal-content div.modal-header div.profile-info.row div.easy-block-v3.no-border div.col-sm-12.padding-top-25 div#calendar.cal-context div#cal-day-box div#cal-day-panel.clearfix a.event-item div.text-center.pull-left.day-event.day-highlight.dh-event-info.cell-appointment")).click();
                    Thread.sleep(2000);
                    driver.findElement(By.id("id_problem")).clear();
                    driver.findElement(By.id("id_problem")).sendKeys("headache");
                    driver.findElement(By.id("id_problem")).clear();
                    driver.findElement(By.id("id_problem")).sendKeys("headache");
                    driver.findElement(By.id("id_comments")).clear();
                    driver.findElement(By.id("id_comments")).sendKeys("After strenuous exercise, a strong headache in the back of the head");//+ appointmentcount);
                    driver.findElement(By.id("id_comments")).clear();
                    driver.findElement(By.id("id_comments")).sendKeys("After strenuous exercise, a strong headache in the back of the head");
                    IsElementPresent(By.id("id_is_second_opinion"));
                    IsElementPresent(By.id("id_follow_up"));
                    driver.findElement(By.xpath("(//button[@type='submit'])[4]")).click();
                    Thread.sleep(10000);
                    //Robot_payment_from_appointment();
                    driver.findElement(By.id("continuePayment")).click();
                    Thread.sleep(2000);
                    driver.findElement(By.partialLinkText("Continue")).click();
                    Thread.sleep(2000);
                    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Fill some patient data for new user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              /*      try {
                        try {
                            driver.findElement(By.id("id_health_conditions_0")).click();
                            driver.findElement(By.id("id_medications_0")).click();
                            driver.findElement(By.id("id_surgeries_0")).click();
                            driver.findElement(By.cssSelector("html body div.wrapper div div.container.content.profile div.row div.talk-to-doctor-container div#proccessModal.modal.fade.in div.modal-dialog.modal-lg div.modal-content div.modal-body div.row div.form_content div div.col-sm-12.col-md-12 form.form-inline.health-history div.form-group.pull-right button.btn.btn-default")).click();
                        } catch (Exception e) {
                        }
                        try {
                            //Thread.sleep(2000);
                            driver.findElement(By.id("id_height_ft")).clear();
                            driver.findElement(By.id("id_height_ft")).sendKeys("10");
                            driver.findElement(By.id("id_height_in")).clear();
                            driver.findElement(By.id("id_height_in")).sendKeys("10");
                            driver.findElement(By.id("id_weight")).clear();
                            driver.findElement(By.id("id_weight")).sendKeys("10");
                            driver.findElement(By.id("id_question_1_0")).click();
                            driver.findElement(By.id("id_question_2_0")).click();
                            driver.findElement(By.id("id_question_3_0")).click();
                            driver.findElement(By.id("id_question_4_0")).click();
                            driver.findElement(By.id("id_question_5_0")).click();
                            driver.findElement(By.id("id_question_6_0")).click();
                            driver.findElement(By.id("id_question_7_0")).click();
                            driver.findElement(By.id("id_question_8_0")).click();
                            driver.findElement(By.xpath("(//button[@type='submit'])[5]")).click();
                        } catch (Exception e) {
                        }
                        Thread.sleep(2000);

                        driver.findElement(By.xpath("(//button[@type='submit'])[5]")).click();
                        driver.findElement(By.xpath("(//button[@type='submit'])[5]")).click();
                    } catch (Exception e) {

                    }*/
                    try {
                        driver.findElement(By.partialLinkText("Continue")).click();
                    } catch (Exception e) {
                    }
                    driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/ul/li[3]/a/h3")).click();
                    driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]/a")).click();
                    new Select(driver.findElement(By.name("type"))).selectByVisibleText("Test");
                    driver.findElement(By.id("id_description")).sendKeys("Manometria prueba");// + appointmentcount);
                    driver.findElement(By.id("id_request_form")).clear();
                    driver.findElement(By.id("id_request_form")).sendKeys("/home/user/Рабочий стол/EMEDICAL DOC DATA/Patient CASE data/Clinic Report.docx");
                    IsElementPresent(By.id("id_result_report_or_record"));
                    driver.findElement(By.id("id_requested_by")).sendKeys("Azcona Guerra");// + appointmentcount);
                    driver.findElement(By.id("id_completed_by")).sendKeys("Salvator Mundi International Hospital");// + appointmentcount);
                    IsElementPresent(By.id("id_additionalfile_set-0-file"));
                    driver.findElement(By.xpath("//button[@type='submit']")).click();
                    Thread.sleep(10000);
                    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Appointment on 2d doctor~~~~~~~~~~~~~~~~~~~~~~~~
                    driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[2]/div/ul/li[2]/a")).click();
                    driver.findElement(By.partialLinkText("GOMEZ CASTELL")).click();
                    try {
                        isElementPresent(By.cssSelector("button.btn-u.show-schedule"));
                    } catch (Exception e) {
                    }
                    Thread.sleep(2000);
                    driver.findElement(By.cssSelector("button.btn-u.show-schedule")).click();
                    Thread.sleep(4000);
                    driver.findElement(By.cssSelector("html body.modal-open div.wrapper div div.container.content.profile div.row div.talk-to-doctor-container div#cur-doctor.modal.fade.in div.modal-dialog.modal-lg.doctor-info div.modal-content div.modal-header div.profile-info.row div.easy-block-v3.no-border div.col-sm-12.padding-top-25 div#calendar.cal-context div#cal-day-box div#cal-day-panel.clearfix a.event-item div.text-center.pull-left.day-event.day-highlight.dh-event-info.cell-appointment")).click();
                    Thread.sleep(4000);
                    driver.findElement(By.id("id_problem")).clear();
                    driver.findElement(By.id("id_problem")).sendKeys("distortion in the leg");// + appointmentcount );
                    driver.findElement(By.id("id_comments")).clear();
                    driver.findElement(By.id("id_comments")).sendKeys("I've injured my leg on the training");// + appointmentcount);
                    IsElementPresent(By.id("id_is_second_opinion"));
                    IsElementPresent(By.id("id_follow_up"));
                    driver.findElement(By.xpath("(//button[@type='submit'])[4]")).click();
                    Thread.sleep(7000);
                    driver.findElement(By.id("continuePayment")).click();
                    Thread.sleep(3000);
                    driver.findElement(By.partialLinkText("Continue")).click();
                    driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/ul/li[3]/a/h3")).click();
                    driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]/a")).click();
                    new Select(driver.findElement(By.name("type"))).selectByVisibleText("Test");
                    driver.findElement(By.id("id_description")).sendKeys("Clinic report");// + appointmentcount);
                    driver.findElement(By.id("id_request_form")).clear();
                    driver.findElement(By.id("id_request_form")).sendKeys("/home/user/Рабочий стол/EMEDICAL DOC DATA/Patient CASE data/Clinic Report.docx");
                    IsElementPresent(By.id("id_result_report_or_record"));
                    driver.findElement(By.id("id_requested_by")).sendKeys("Gomez Castell");// + appointmentcount);
                    driver.findElement(By.id("id_completed_by")).sendKeys("Salvator Mundi International Hospital");// + appointmentcount);
                    IsElementPresent(By.id("id_additionalfile_set-0-file"));
                    driver.findElement(By.xpath("//button[@type='submit']")).click();
                    Thread.sleep(10000);
                    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~3d doc appointment~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    driver.findElement(By.partialLinkText("Talk to a doctor")).click();
                    driver.findElement(By.partialLinkText("DIEZ DEL CASTILLIO")).click();
                    try {
                        isElementPresent(By.cssSelector("button.btn-u.show-schedule"));
                    } catch (Exception e) {
                    }
                    Thread.sleep(2000);
                    driver.findElement(By.cssSelector("button.btn-u.show-schedule")).click();
                    Thread.sleep(4000);
                    driver.findElement(By.cssSelector("html body.modal-open div.wrapper div div.container.content.profile div.row div.talk-to-doctor-container div#cur-doctor.modal.fade.in div.modal-dialog.modal-lg.doctor-info div.modal-content div.modal-header div.profile-info.row div.easy-block-v3.no-border div.col-sm-12.padding-top-25 div#calendar.cal-context div#cal-day-box div#cal-day-panel.clearfix a.event-item div.text-center.pull-left.day-event.day-highlight.dh-event-info.cell-appointment")).click();
                    driver.findElement(By.id("id_problem")).clear();
                    driver.findElement(By.id("id_problem")).sendKeys("The arm pain");// + appointmentcount);
                    driver.findElement(By.id("id_comments")).clear();
                    driver.findElement(By.id("id_comments")).sendKeys("The arm was injured in training");// + appointmentcount);
                    IsElementPresent(By.id("id_is_second_opinion"));
                    IsElementPresent(By.id("id_follow_up"));
                    driver.findElement(By.xpath("(//button[@type='submit'])[4]")).click();
                    Thread.sleep(7000);
                    driver.findElement(By.id("continuePayment")).click();
                    Thread.sleep(3000);
                    driver.findElement(By.partialLinkText("Continue")).click();
                    driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/ul/li[3]/a/h3")).click();
                    driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]/a")).click();
                    new Select(driver.findElement(By.name("type"))).selectByVisibleText("Test");
                    driver.findElement(By.id("id_description")).sendKeys("Manometria prueba");// + appointmentcount);
                    driver.findElement(By.id("id_request_form")).clear();
                    driver.findElement(By.id("id_request_form")).sendKeys("/home/user/Рабочий стол/EMEDICAL DOC DATA/Patient CASE data/UAT MANOMETRIA PRUEBA.docx");
                    IsElementPresent(By.id("id_result_report_or_record"));
                    driver.findElement(By.id("id_requested_by")).sendKeys("Diez Del Castillio");// + appointmentcount);
                    driver.findElement(By.id("id_completed_by")).sendKeys("Salvator Mundi International Hospital");// + appointmentcount);
                    IsElementPresent(By.id("id_additionalfile_set-0-file"));
                    driver.findElement(By.xpath("//button[@type='submit']")).click();
                    Thread.sleep(10000);
                    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4d doc appointment~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[2]/div/ul/li[2]/a")).click();
                    driver.findElement(By.partialLinkText("TORREZ FIERRE")).click();
                    try {
                        isElementPresent(By.cssSelector("button.btn-u.show-schedule"));
                    } catch (Exception e) {
                    }
                    Thread.sleep(2000);
                    driver.findElement(By.cssSelector("button.btn-u.show-schedule")).click();
                    Thread.sleep(4000);
                    driver.findElement(By.cssSelector("html body.modal-open div.wrapper div div.container.content.profile div.row div.talk-to-doctor-container div#cur-doctor.modal.fade.in div.modal-dialog.modal-lg.doctor-info div.modal-content div.modal-header div.profile-info.row div.easy-block-v3.no-border div.col-sm-12.padding-top-25 div#calendar.cal-context div#cal-day-box div#cal-day-panel.clearfix a.event-item div.text-center.pull-left.day-event.day-highlight.dh-event-info.cell-appointment")).click();
                    Thread.sleep(4000);
                    driver.findElement(By.id("id_problem")).clear();
                    driver.findElement(By.id("id_problem")).sendKeys("abdominal pain");// + appointmentcount);
                    driver.findElement(By.id("id_comments")).clear();
                    driver.findElement(By.id("id_comments")).sendKeys("abdominal pain after falling from a bicycle");// + appointmentcount);
                    IsElementPresent(By.id("id_is_second_opinion"));
                    IsElementPresent(By.id("id_follow_up"));
                    driver.findElement(By.xpath("(//button[@type='submit'])[4]")).click();
                    Thread.sleep(7000);
                    driver.findElement(By.id("continuePayment")).click();
                    Thread.sleep(3000);
                    driver.findElement(By.partialLinkText("Continue")).click();
                    driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/ul/li[3]/a/h3")).click();
                    driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]/a")).click();
                    new Select(driver.findElement(By.name("type"))).selectByVisibleText("Test");
                    driver.findElement(By.id("id_description")).sendKeys("Clinic report");// + appointmentcount);
                    driver.findElement(By.id("id_request_form")).clear();
                    driver.findElement(By.id("id_request_form")).sendKeys("/home/user/Рабочий стол/EMEDICAL DOC DATA/Patient CASE data/Clinic Report.docx");
                    IsElementPresent(By.id("id_result_report_or_record"));
                    driver.findElement(By.id("id_requested_by")).sendKeys("Torrez Fierre");// + appointmentcount);
                    driver.findElement(By.id("id_completed_by")).sendKeys("Salvator Mundi International Hospital");// + appointmentcount);
                    IsElementPresent(By.id("id_additionalfile_set-0-file"));
                    driver.findElement(By.xpath("//button[@type='submit']")).click();
                    Thread.sleep(10000);
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~5d doc appointment~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[2]/div/ul/li[2]/a")).click();
                    driver.findElement(By.partialLinkText("SANZ MORA")).click();
                    try {
                        isElementPresent(By.cssSelector("button.btn-u.show-schedule"));
                    } catch (Exception e) {
                    }
                    Thread.sleep(2000);
                    driver.findElement(By.cssSelector("button.btn-u.show-schedule")).click();
                    Thread.sleep(4000);
                    driver.findElement(By.cssSelector("html body.modal-open div.wrapper div div.container.content.profile div.row div.talk-to-doctor-container div#cur-doctor.modal.fade.in div.modal-dialog.modal-lg.doctor-info div.modal-content div.modal-header div.profile-info.row div.easy-block-v3.no-border div.col-sm-12.padding-top-25 div#calendar.cal-context div#cal-day-box div#cal-day-panel.clearfix a.event-item div.text-center.pull-left.day-event.day-highlight.dh-event-info.cell-appointment")).click();
                    Thread.sleep(4000);
                    driver.findElement(By.id("id_problem")).clear();
                    driver.findElement(By.id("id_problem")).sendKeys("Migraine");// + appointmentcount);
                    driver.findElement(By.id("id_comments")).clear();
                    driver.findElement(By.id("id_comments")).sendKeys("Headache in temples");// + appointmentcount);
                    IsElementPresent(By.id("id_is_second_opinion"));
                    IsElementPresent(By.id("id_follow_up"));
                    driver.findElement(By.xpath("(//button[@type='submit'])[4]")).click();
                    Thread.sleep(7000);
                    driver.findElement(By.id("continuePayment")).click();
                    Thread.sleep(2000);
                    driver.findElement(By.partialLinkText("Continue")).click();
                    driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/ul/li[3]/a/h3")).click();
                    driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]/a")).click();
                    new Select(driver.findElement(By.name("type"))).selectByVisibleText("Test");
                    driver.findElement(By.id("id_description")).sendKeys("Manometria Prueba");// + appointmentcount);
                    driver.findElement(By.id("id_request_form")).clear();
                    driver.findElement(By.id("id_request_form")).sendKeys("/home/user/Рабочий стол/EMEDICAL DOC DATA/Patient CASE data/UAT MANOMETRIA PRUEBA.docx");
                    IsElementPresent(By.id("id_result_report_or_record"));
                    driver.findElement(By.id("id_requested_by")).sendKeys("Sanz Moara");// + appointmentcount);
                    driver.findElement(By.id("id_completed_by")).sendKeys("Salvator Mundi International Hospital");// + appointmentcount);
                    IsElementPresent(By.id("id_additionalfile_set-0-file"));
                    driver.findElement(By.xpath("//button[@type='submit']")).click();
                    Thread.sleep(10000);
                    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~6d doc appointment~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[2]/div/ul/li[2]/a")).click();
                    driver.findElement(By.partialLinkText("RIU VILLAR")).click();
                    try {
                        isElementPresent(By.cssSelector("button.btn-u.show-schedule"));
                    } catch (Exception e) {
                    }
                    Thread.sleep(2000);
                    driver.findElement(By.cssSelector("button.btn-u.show-schedule")).click();
                    Thread.sleep(4000);
                    driver.findElement(By.cssSelector("html body.modal-open div.wrapper div div.container.content.profile div.row div.talk-to-doctor-container div#cur-doctor.modal.fade.in div.modal-dialog.modal-lg.doctor-info div.modal-content div.modal-header div.profile-info.row div.easy-block-v3.no-border div.col-sm-12.padding-top-25 div#calendar.cal-context div#cal-day-box div#cal-day-panel.clearfix a.event-item div.text-center.pull-left.day-event.day-highlight.dh-event-info.cell-appointment")).click();
                    Thread.sleep(4000);
                    driver.findElement(By.id("id_problem")).clear();
                    driver.findElement(By.id("id_problem")).sendKeys("shoulder injury");// + appointmentcount);
                    driver.findElement(By.id("id_comments")).clear();
                    driver.findElement(By.id("id_comments")).sendKeys("shoulder pain after an accident with car crash");// + appointmentcount);
                    IsElementPresent(By.id("id_is_second_opinion"));
                    IsElementPresent(By.id("id_follow_up"));
                    driver.findElement(By.xpath("(//button[@type='submit'])[4]")).click();
                    Thread.sleep(7000);
                    driver.findElement(By.id("continuePayment")).click();
                    Thread.sleep(2000);
                    driver.findElement(By.partialLinkText("Continue")).click();
                    driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/ul/li[3]/a/h3")).click();
                    driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]/a")).click();
                    new Select(driver.findElement(By.name("type"))).selectByVisibleText("Test");
                    driver.findElement(By.id("id_description")).sendKeys("Clinic report");// + appointmentcount);
                    driver.findElement(By.id("id_request_form")).clear();
                    driver.findElement(By.id("id_request_form")).sendKeys("/home/user/Рабочий стол/EMEDICAL DOC DATA/Patient CASE data/Clinic Report.docx");
                    IsElementPresent(By.id("id_result_report_or_record"));
                    driver.findElement(By.id("id_requested_by")).sendKeys("Riu Villar");// + appointmentcount);
                    driver.findElement(By.id("id_completed_by")).sendKeys("Salvator Mundi International Hospital");// + appointmentcount);
                    IsElementPresent(By.id("id_additionalfile_set-0-file"));
                    driver.findElement(By.xpath("//button[@type='submit']")).click();


                    Logout();
                }
            }
            driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
            //endregion

            Case_Interactions_from_DOC();

            Thread.sleep(2000);
            Registration_and_confrimation();
            Make_appointment_for_new_patient();//no FOR
            Login_as_admin();
            Case_Interactions_from_DOC();//Includes cycle
            Create_Doc_from_admin();
            Login_as_patient();   //No cycle
            Case_interactions();  //need to login 1st
            Cancel_case_from_logged_patient();
            Robot_payment_from_profile();
            My_health_fillin();
            password_changing();
            Logout();
            Search_doc(); //useless for now
            Fill_doc_profile(); //need a cycle ~~it WORKS WELL
            Patient_account_info();

        }
          //region after
 /*   @After
    public void tearDown() throws Exception {
        driver.quit();
        String verificationErrorString = verificationErrors.toString();
        if (!"".equals(verificationErrorString)) {
            fail(verificationErrorString);
        }
    }*/
//endregion

    public void Case_Interactions_from_DOC()
    {
        try {
            for (emailnumber = 1; emailnumber < 7; emailnumber++) {
                Login_as_doc();
                for (appointmentcount = 1; appointmentcount < 10; appointmentcount++) {
                    driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[2]/div/ul/li[2]/a")).click();
                    driver.findElement(By.partialLinkText("Appointments")).click();
                    try {
                        driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/table/tbody/tr[" + appointmentcount + "]/td[5]/a[1]")).click();
                    } catch (Exception e) {
                        break;
                    }
                    driver.findElement(By.partialLinkText("Appointments & Notes")).click();
                    driver.findElement(By.partialLinkText("Edit note")).click();
                    driver.findElement(By.id("id_anamnesis")).clear();
                    driver.findElement(By.id("id_anamnesis")).sendKeys("AP:. F - B:-" + Keys.ENTER + "Amigdalectomía." + Keys.ENTER + "Talasemia minor." + Keys.ENTER + "Jaquecas frecuentes en tratamiento con Carbapacemina y par l columna Artrotec." + Keys.ENTER + "No alergias conocidas. ");
                    driver.findElement(By.id("id_exploration")).clear();
                    driver.findElement(By.id("id_exploration")).sendKeys("Epigastralgia. Resto igual");
                    driver.findElement(By.id("id_diagnosis")).clear();
                    driver.findElement(By.id("id_diagnosis")).sendKeys("Gastritis helicobacter +");
                    driver.findElement(By.id("id_additional_tests")).clear();
                    driver.findElement(By.id("id_additional_tests")).sendKeys("AF:. \n" +
                            "21,1,13 \n" +
                            "EA:: .Cuadro de dolor epigastrico que irradia todo el abdomen . No cede con la ingesta y sy lo hace cuando vomita.\n" +
                            "Esta en tratamiento con Movicol. \n" +
                            "11,2,13: BREATH TEST 7,57 Positivo. \n" +
                            "ECOGRAFIA ABDOMINAL: Sin alteraciones.\n" +
                            "22,4,13: BREATH TEST: 15,3 Positivo. \n" +
                            "20,5,13: cuádruple terapia.\n" +
                            "21,10,13: BREATH TEST: 0,9 Negativo.\n" +
                            "3,3,15: Cuadro de descomposición y vómitos , con presencia de moco en heces. Suxidina0,1,1,");
                    driver.findElement(By.id("id_treatment")).clear();
                    driver.findElement(By.id("id_treatment")).sendKeys("Triple terapia");
                    driver.findElement(By.id("id_public_notes")).clear();
                    driver.findElement(By.id("id_public_notes")).sendKeys("Public notes");
                    driver.findElement(By.xpath("//button[@type='submit']")).click();
                    Thread.sleep(2000);
                    driver.findElement(By.partialLinkText("Records and Tests")).click();
                    try {
                        driver.findElement(By.partialLinkText("Edit")).click();
                        driver.findElement(By.id("id_conclusions")).clear();
                        driver.findElement(By.id("id_conclusions")).sendKeys("Two analgin tablets after meals");// + emailnumber);
                        driver.findElement(By.xpath("//button[@type='submit']")).click();
                        Thread.sleep(1000);
                    } catch (Exception e) {
                    }
                }
                Logout();
            }
        }
        catch (InterruptedException e)
        {}
    }

    public void Login_as_doc()
    {
        driver.get(baseUrl + "/en/");
        driver.findElement(By.partialLinkText("LOGIN")).click();
        driver.findElement(By.id("id_login")).clear();
        driver.findElement(By.id("id_login")).sendKeys("emedicaltest" + emailnumber +"@mail2tor.com");
        driver.findElement(By.id("id_password")).clear();
        driver.findElement(By.id("id_password")).sendKeys(Password);
        driver.findElement(By.xpath("//button[@type='submit']")).click();
    }

    public  void Make_appointment_for_new_patient()
    {

        try {
            Login_as_patient();
            driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[2]/div/ul/li[2]")).click();
            driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div[2]/div/a")).click();
            try {
                IsElementPresent(By.id("select2-appointment_time-container"));
                driver.findElement(By.id("make_appointment")).click();
            } catch (Exception e) {
            }
            Thread.sleep(2000);
            driver.findElement(By.id("id_problem")).sendKeys("Migraine");
            driver.findElement(By.id("id_comments")).sendKeys("Strong headache");
            IsElementPresent(By.id("id_is_second_opinion"));
            IsElementPresent(By.id("id_follow_up"));
            driver.findElement(By.xpath("(//button[@type='submit'])[4]")).click();
            Thread.sleep(5000);
            Robot_payment_from_appointment();
            Thread.sleep(2000);
            driver.findElement(By.partialLinkText("Continue")).click();
            Thread.sleep(2000);
            //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Fill some patient data for new user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            try {
                driver.findElement(By.id("id_health_conditions_0")).click();
                driver.findElement(By.id("id_medications_0")).click();
                driver.findElement(By.id("id_surgeries_0")).click();
                driver.findElement(By.cssSelector("html body div.wrapper div div.container.content.profile div.row div.talk-to-doctor-container div#proccessModal.modal.fade.in div.modal-dialog.modal-lg div.modal-content div.modal-body div.row div.form_content div div.col-sm-12.col-md-12 form.form-inline.health-history div.form-group.pull-right button.btn.btn-default")).click();
                driver.findElement(By.id("id_height_ft")).clear();
                driver.findElement(By.id("id_height_ft")).sendKeys("10");
                driver.findElement(By.id("id_height_in")).clear();
                driver.findElement(By.id("id_height_in")).sendKeys("10");
                driver.findElement(By.id("id_weight")).clear();
                driver.findElement(By.id("id_weight")).sendKeys("10");
                driver.findElement(By.id("id_question_1_0")).click();
                driver.findElement(By.id("id_question_2_0")).click();
                driver.findElement(By.id("id_question_3_0")).click();
                driver.findElement(By.id("id_question_4_0")).click();
                driver.findElement(By.id("id_question_5_0")).click();
                driver.findElement(By.id("id_question_6_0")).click();
                driver.findElement(By.id("id_question_7_0")).click();
                driver.findElement(By.id("id_question_8_0")).click();
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[9]/div/div/div[2]/div[2]/div/div/div/form/div[3]/button")).click();
                Thread.sleep(2000);
                driver.findElement(By.xpath("(//button[@type='submit'])[5]")).click();
                driver.findElement(By.xpath("(//button[@type='submit'])[5]")).click();
                driver.findElement(By.partialLinkText("Continue")).click();
            }
            catch (Exception e)
            {
                e.printStackTrace();
            }

        }
        catch (InterruptedException e)
        {}
    }

    public void Robot_payment_from_appointment()
    {
        try {
            try {
                Robot robot2 = new Robot();

/*                robot2.keyPress(KeyEvent.VK_ALT);
                robot2.keyPress(KeyEvent.VK_TAB);
                robot2.keyRelease(KeyEvent.VK_TAB);
                robot2.keyRelease(KeyEvent.VK_ALT);

                Thread.sleep(1000);

                robot2.keyPress(KeyEvent.VK_ALT);
                robot2.keyPress(KeyEvent.VK_TAB);
                robot2.keyRelease(KeyEvent.VK_TAB);
                robot2.keyRelease(KeyEvent.VK_ALT);
                Thread.sleep(1000);*/

             /*   robot2.keyPress(KeyEvent.VK_ALT);
                robot2.keyPress(KeyEvent.VK_SPACE);
                robot2.keyRelease(KeyEvent.VK_ALT);
                robot2.keyRelease(KeyEvent.VK_SPACE);
                Thread.sleep(1000);


                robot2.keyPress(KeyEvent.VK_DOWN);
                robot2.keyRelease(KeyEvent.VK_DOWN);
                 Thread.sleep(100);

                robot2.keyPress(KeyEvent.VK_DOWN);
                robot2.keyRelease(KeyEvent.VK_DOWN);
                Thread.sleep(100);

                robot2.keyPress(KeyEvent.VK_ENTER);
                robot2.keyRelease(KeyEvent.VK_ENTER);
                Thread.sleep(100);*/
                robot2.keyPress(KeyEvent.VK_TAB);
                robot2.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot2.keyPress(KeyEvent.VK_TAB);
                robot2.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot2.keyPress(KeyEvent.VK_TAB);
                robot2.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(300);
                robot2.keyPress(KeyEvent.VK_5);
                robot2.keyRelease(KeyEvent.VK_5);
                robot2.keyPress(KeyEvent.VK_4);
                robot2.keyRelease(KeyEvent.VK_4);
                robot2.keyPress(KeyEvent.VK_5);
                robot2.keyRelease(KeyEvent.VK_5);
                robot2.keyPress(KeyEvent.VK_4);
                robot2.keyRelease(KeyEvent.VK_4);
                robot2.keyPress(KeyEvent.VK_5);
                robot2.keyRelease(KeyEvent.VK_5);
                robot2.keyPress(KeyEvent.VK_4);
                robot2.keyRelease(KeyEvent.VK_4);
                robot2.keyPress(KeyEvent.VK_5);
                robot2.keyRelease(KeyEvent.VK_5);
                robot2.keyPress(KeyEvent.VK_4);
                robot2.keyRelease(KeyEvent.VK_4);
                robot2.keyPress(KeyEvent.VK_5);
                robot2.keyRelease(KeyEvent.VK_5);
                robot2.keyPress(KeyEvent.VK_4);
                robot2.keyRelease(KeyEvent.VK_4);
                robot2.keyPress(KeyEvent.VK_5);
                robot2.keyRelease(KeyEvent.VK_5);
                robot2.keyPress(KeyEvent.VK_4);
                robot2.keyRelease(KeyEvent.VK_4);
                robot2.keyPress(KeyEvent.VK_5);
                robot2.keyRelease(KeyEvent.VK_5);
                robot2.keyPress(KeyEvent.VK_4);
                robot2.keyRelease(KeyEvent.VK_4);
                robot2.keyPress(KeyEvent.VK_5);
                robot2.keyRelease(KeyEvent.VK_5);
                robot2.keyPress(KeyEvent.VK_4);
                robot2.keyRelease(KeyEvent.VK_4);
                Thread.sleep(1000);
                robot2.keyPress(KeyEvent.VK_TAB);
                robot2.keyRelease(KeyEvent.VK_TAB);
                robot2.keyPress(KeyEvent.VK_1);
                robot2.keyRelease(KeyEvent.VK_1);
                robot2.keyPress(KeyEvent.VK_2);
                robot2.keyRelease(KeyEvent.VK_2);
                robot2.keyPress(KeyEvent.VK_1);
                robot2.keyRelease(KeyEvent.VK_1);
                robot2.keyPress(KeyEvent.VK_7);
                robot2.keyRelease(KeyEvent.VK_7);
                Thread.sleep(1000);
               driver.findElement(By.id("continuePayment")).click();


            } catch (AWTException ex)
            {
                ex.printStackTrace();
            }
        }
        catch (InterruptedException e)
        {e.printStackTrace();}
    }

    public void Cancel_case_from_logged_patient()
    {
        Login_as_patient();
        driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[2]/div/ul/li[3]")).click();
        driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/ul/li[4]/a")).click();
        for (i = 2; i < 11; i++) {
            try {
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[" + tablelanenumber + "]/td[2]"));//2я колонка таблицы кейсов
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                driver.findElement(By.xpath("html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[3]/ul/li[" + i + "]/a")).click();
                tablelanenumber = 1;
            } catch (Exception e) {
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[" + tablelanenumber + "]/td[2]/../td[4]/a")).click();
                break;
            }
        }
        driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/ul/li[2]/a")).click();
        try {
            driver.findElement(By.linkText("Cancel")).click();
        } catch (Exception e) {
            IsElementPresent(By.linkText("Cancel"));
        }
    }

    public void Case_interactions() //EDITABLE
    {
        driver.findElement(By.partialLinkText("My health")).click();
        driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/ul/li[4]/a")).click();
        for (i = 2; i < 11; i++) {
            try {
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[" + tablelanenumber + "]/td[2]"));//2я колонка таблицы кейсов
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                NOTextSearch("Test Problem", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[ " + tablelanenumber + " ]/td[2]"));
                tablelanenumber++;
                driver.findElement(By.xpath("html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[3]/ul/li[" + i + "]/a")).click();
                tablelanenumber = 1;
            } catch (Exception e) {
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[" + tablelanenumber + "]/td[2]/../td[4]/a")).click();
                break;
            }
        }
        IsElementPresent(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]"));
        IsElementPresent(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[3]"));
        IsElementPresent(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[5]"));
        IsElementPresent(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[7]"));
        driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/ul/li[2]/a")).click();
        if (driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/table/tbody/tr/td[3]")).getText() == "New")

        {
            driver.findElement(By.partialLinkText("Edit")).click();
            new Select(driver.findElement(By.id("id_case"))).selectByVisibleText("Headache");
            new Select(driver.findElement(By.id("id_appointment_type"))).selectByVisibleText("Phone");
            IsElementPresent(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/form/div[2]/button"));
        } else {
            driver.findElement(By.partialLinkText("Files / Tests")).click();
        }
        driver.navigate().back();
        driver.findElement(By.partialLinkText("Files / Tests")).click();
        TextSearch("No previous documents found", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/h2"));
        driver.findElement(By.partialLinkText("Upload new file / test")).click();
        new Select(driver.findElement(By.name("type"))).selectByVisibleText("Test");
        driver.findElement(By.id("id_description")).sendKeys("Autotest Description");
        driver.findElement(By.id("id_request_form")).sendKeys("/home/user/Рабочий стол/Test text  formats/hrpro-Спек_NsoCxwq.pdf");
        IsElementPresent(By.id("id_result_report_or_record"));
        driver.findElement(By.id("id_requested_by")).sendKeys("Autotest request");
        driver.findElement(By.id("id_completed_by")).sendKeys("Completed by Autotest");
        IsElementPresent(By.id("id_additionalfile_set-0-file"));
        driver.findElement(By.xpath("//button[@type='submit']")).click();
        TextSearch("Autotest request", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/table/tbody/tr/td[4]"));
        TextSearch("Completed by Autotest", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/table/tbody/tr/td[5]"));
        driver.findElement(By.partialLinkText("Delete")).click();
        driver.findElement(By.xpath("(//button[@type='submit'])[2]")).click();
        TextSearch("No previous documents found", By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/h2"));
        driver.findElement(By.partialLinkText("Doctor Notes")).click();
        driver.findElement(By.partialLinkText("Messages")).click();
        IsElementPresent(By.partialLinkText("Send new"));
        IsElementPresent(By.partialLinkText("Closed"));
    }

    public void My_health_fillin()
    {
        driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[2]/div/ul/li[3]")).click();
        driver.findElement(By.id("id_health_conditions_0")).click();
        driver.findElement(By.id("id_medications_1")).click();
        driver.findElement(By.id("id_medications_info")).clear();
        driver.findElement(By.id("id_medications_info")).sendKeys("Vitamin B2, Vitamin D2, Tylenol PM");
        driver.findElement(By.id("id_surgeries_0")).click();
        driver.findElement(By.xpath("//button[@type='submit']")).click();

        driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[2]/ul/li[2]")).click();
        driver.findElement(By.id("id_height_ft")).clear();
        driver.findElement(By.id("id_height_ft")).sendKeys("10");
        driver.findElement(By.id("id_height_in")).clear();
        driver.findElement(By.id("id_height_in")).sendKeys("10");
        driver.findElement(By.id("id_weight")).clear();
        driver.findElement(By.id("id_weight")).sendKeys("10");
        driver.findElement(By.id("id_question_1_0")).click();
        driver.findElement(By.id("id_question_2_1")).click();
        driver.findElement(By.id("id_question_3_0")).click();
        driver.findElement(By.id("id_question_4_0")).click();
        driver.findElement(By.id("id_question_5_1")).click();
        driver.findElement(By.id("id_question_6_1")).click();
        driver.findElement(By.id("id_question_7_0")).click();
        driver.findElement(By.id("id_question_8_0")).click();
        driver.findElement(By.xpath("//button[@type='submit']")).click();

        driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[2]/ul/li[3]/a")).click();
        new Select(driver.findElement(By.id("id_condition_1"))).selectByVisibleText("Aunt");
       /* new Select(driver.findElement(By.id("id_condition_2"))).selectByVisibleText("Aunt");
        new Select(driver.findElement(By.id("id_condition_3"))).selectByVisibleText("Aunt");
        new Select(driver.findElement(By.id("id_condition_4"))).selectByVisibleText("Aunt");
        new Select(driver.findElement(By.id("id_condition_5"))).selectByVisibleText("Aunt");
        new Select(driver.findElement(By.id("id_condition_6"))).selectByVisibleText("Aunt");
        new Select(driver.findElement(By.id("id_condition_7"))).selectByVisibleText("Aunt");
        new Select(driver.findElement(By.id("id_condition_8"))).selectByVisibleText("Aunt");
        new Select(driver.findElement(By.id("id_condition_9"))).selectByVisibleText("Aunt");
        new Select(driver.findElement(By.id("id_condition_10"))).selectByVisibleText("Aunt");
        new Select(driver.findElement(By.id("id_condition_11"))).selectByVisibleText("Aunt");
        new Select(driver.findElement(By.id("id_condition_12"))).selectByVisibleText("Aunt");*/
        new Select(driver.findElement(By.id("id_condition_13"))).selectByVisibleText("Aunt");
        driver.findElement(By.xpath("//button[@type='submit']")).click();
        TextSearch("100%", (By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div/h4/strong")));}

    //region useless
   /* public void Create_appointment() //UNFINISHED WTF
    {
        try {
            for (i = 0; i < 2; i++)
            {
                driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[2]/div/ul/li[2]")).click();
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div[2]/div/a")).click();

                try {
                    IsElementPresent(By.id("select2-appointment_time-container"));
                    driver.findElement(By.id("make_appointment")).click();
                } catch (Exception e) {
                }
                Thread.sleep(1000);
                driver.findElement(By.id("id_problem")).sendKeys("Test Problem");
                driver.findElement(By.id("id_comments")).sendKeys("Test Comment");
                IsElementPresent(By.id("id_is_second_opinion"));
                IsElementPresent(By.id("id_follow_up"));
                driver.findElement(By.xpath("(//button[@type='submit'])[2]")).click();
                Thread.sleep(4000);


                driver.findElement(By.xpath("//input[contains(@placeholder,'Card Number')]")).sendKeys("5454545445454545454");
                driver.findElement(By.cssSelector("html.is-modern.card-root.js.no-touch.csstransitions.svg.inlinesvg.placeholder body.inline-frame div#container div.add-payment-method-view div.payment-container div.form-container div.add-payment-method-form-view form.grid.card-form label.card-label.credit-card-number-label input#credit-card-number.card-field")).sendKeys("5454545454545454");
                driver.findElement(By.xpath(".*//*//**//*[@id='credit-card-number']")).sendKeys("5454545454545454");
                driver.findElement(By.xpath("/html/body/div[1]/div[1]/div/div[2]/div/form/div/div/label/input")).sendKeys("1217");
                driver.findElement(By.id("continuePayment")).click();
                Thread.sleep(2000);
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[7]/div/div/div[2]/div[2]/div/a")).click();
                //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Fill some patient data for new user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.id("id_health_conditions_0")).click();
                driver.findElement(By.id("id_medications_0")).click();
                driver.findElement(By.id("id_surgeries_0")).click();
                driver.findElement(By.xpath("(//button[@type='submit'])[3]")).click();
                driver.findElement(By.id("id_height_ft")).clear();
                driver.findElement(By.id("id_height_ft")).sendKeys("10");
                driver.findElement(By.id("id_height_ft")).clear();
                driver.findElement(By.id("id_height_in")).sendKeys("10");
                driver.findElement(By.id("id_weight")).clear();
                driver.findElement(By.id("id_weight")).sendKeys("10");
                driver.findElement(By.id("id_question_1_0")).click();
                driver.findElement(By.id("id_question_2_0")).click();
                driver.findElement(By.id("id_question_3_0")).click();
                driver.findElement(By.id("id_question_4_0")).click();
                driver.findElement(By.id("id_question_5_0")).click();
                driver.findElement(By.id("id_question_6_0")).click();
                driver.findElement(By.id("id_question_7_0")).click();
                driver.findElement(By.id("id_question_8_0")).click();
                driver.findElement(By.xpath("(//button[@type='submit'])[3]")).click();
                driver.findElement(By.xpath("(//button[@type='submit'])[3]")).click();
                driver.findElement(By.partialLinkText("link=Continue")).click();
                IsElementPresent(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/ul/li[1]/a/h3"));
            }
        }
        catch(InterruptedException e)
        {}
    }*/
//endregion
    public void Search_doc()
    { driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[2]/div/ul/li[2]/a")).click();
        IsElementPresent(By.name("doctor_specialty"));
        driver.findElement(By.name("end_date")).click();
        driver.findElement(By.xpath("/html/body/div[3]/div[1]/table/tbody/tr[3]/td[5]")).click();
        driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/form/div[3]/span/span[1]/span")).click();
        driver.findElement(By.xpath("/html/body/span/span/span[1]/input")).sendKeys("Alan");
        driver.findElement(By.xpath("/html/body/span/span/span[1]/input")).sendKeys (Keys.ENTER);
        driver.findElement(By.xpath("//button[@type='submit']")).click();
        Collection<WebElement> list1 = driver.findElements(By.partialLinkText("ALAN ALLCOME"));
        if(list1.size() > 1)
        {
            System.console().writer().println("Search functionality has failed");
            driver.findElement(By.xpath("adasdsd")).click();
            driver.quit();
        }
        else
        {}
    }

    public void Robot_payment_from_profile()
    {
        try {
            Actions builder2 = new Actions(driver);
            builder2.moveToElement(driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[1]/div/ul/li[5]"))).perform();
            driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[1]/div/ul/li[5]/ul/li[1]/a")).click();
            driver.findElement(By.xpath("/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div[1]/div[2]/div/a")).click();
            Thread.sleep(4000);


            try {
                Robot robot = new Robot();

                robot.keyPress(KeyEvent.VK_ALT);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_ALT);

                Thread.sleep(2000);

                robot.keyPress(KeyEvent.VK_ALT);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_ALT);

                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_ALT);
                robot.keyPress(KeyEvent.VK_SPACE);
                robot.keyRelease(KeyEvent.VK_ALT);
                robot.keyRelease(KeyEvent.VK_SPACE);
                Thread.sleep(1000);



                robot.keyPress(KeyEvent.VK_DOWN);
                robot.keyRelease(KeyEvent.VK_DOWN);
                Thread.sleep(100);

                robot.keyPress(KeyEvent.VK_DOWN);
                robot.keyRelease(KeyEvent.VK_DOWN);
                Thread.sleep(100);

                robot.keyPress(KeyEvent.VK_ENTER);
                robot.keyRelease(KeyEvent.VK_ENTER);
                Thread.sleep(100);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                Thread.sleep(1000);

                robot.keyPress(KeyEvent.VK_ENTER);
                robot.keyRelease(KeyEvent.VK_ENTER);

                robot.keyPress(KeyEvent.VK_5);
                robot.keyRelease(KeyEvent.VK_5);
                robot.keyPress(KeyEvent.VK_4);
                robot.keyRelease(KeyEvent.VK_4);
                robot.keyPress(KeyEvent.VK_5);
                robot.keyRelease(KeyEvent.VK_5);
                robot.keyPress(KeyEvent.VK_4);
                robot.keyRelease(KeyEvent.VK_4);
                robot.keyPress(KeyEvent.VK_5);
                robot.keyRelease(KeyEvent.VK_5);
                robot.keyPress(KeyEvent.VK_4);
                robot.keyRelease(KeyEvent.VK_4);
                robot.keyPress(KeyEvent.VK_5);
                robot.keyRelease(KeyEvent.VK_5);
                robot.keyPress(KeyEvent.VK_4);
                robot.keyRelease(KeyEvent.VK_4);
                robot.keyPress(KeyEvent.VK_5);
                robot.keyRelease(KeyEvent.VK_5);
                robot.keyPress(KeyEvent.VK_4);
                robot.keyRelease(KeyEvent.VK_4);
                robot.keyPress(KeyEvent.VK_5);
                robot.keyRelease(KeyEvent.VK_5);
                robot.keyPress(KeyEvent.VK_4);
                robot.keyRelease(KeyEvent.VK_4);
                robot.keyPress(KeyEvent.VK_5);
                robot.keyRelease(KeyEvent.VK_5);
                robot.keyPress(KeyEvent.VK_4);
                robot.keyRelease(KeyEvent.VK_4);
                robot.keyPress(KeyEvent.VK_5);
                robot.keyRelease(KeyEvent.VK_5);
                robot.keyPress(KeyEvent.VK_4);
                robot.keyRelease(KeyEvent.VK_4);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);
                robot.keyPress(KeyEvent.VK_1);
                robot.keyRelease(KeyEvent.VK_1);
                robot.keyPress(KeyEvent.VK_2);
                robot.keyRelease(KeyEvent.VK_2);
                robot.keyPress(KeyEvent.VK_1);
                robot.keyRelease(KeyEvent.VK_1);
                robot.keyPress(KeyEvent.VK_7);
                robot.keyRelease(KeyEvent.VK_7);
                Thread.sleep(1000);
                robot.keyPress(KeyEvent.VK_TAB);
                robot.keyRelease(KeyEvent.VK_TAB);

                robot.keyPress(KeyEvent.VK_ENTER);
                robot.keyRelease(KeyEvent.VK_ENTER);

            } catch (AWTException e) {
                e.printStackTrace();
            }
        }
        catch(InterruptedException ex)
        {}
    }

    public void Logout()
    {
        try {
            Thread.sleep(1000);
            Actions builder3 = new Actions(driver);
            builder3.moveToElement(driver.findElement(By.xpath("//li[5]"))).perform();
            Thread.sleep(2000);
            driver.findElement(By.partialLinkText("LOGOUT")).click();
        }
        catch (InterruptedException e)
        {e.printStackTrace();}
    }

    public void Fill_doc_profile()
    {
        for(emailnumber =1;emailnumber < 7;emailnumber ++)
        {
            try {
                Logout();
            }
            catch (Exception e)
            {}
            driver.get(baseUrl + "/en/");
            driver.findElement(By.partialLinkText("LOGIN")).click();
            driver.findElement(By.id("id_login")).clear();
            driver.findElement(By.id("id_login")).sendKeys("emedicaltest" + emailnumber +"@mail2tor.com");
            driver.findElement(By.id("id_password")).clear();
            driver.findElement(By.id("id_password")).sendKeys(Password);
            driver.findElement(By.xpath("//button[@type='submit']")).click();
           /* try {
            IsElementPresent(By.xpath("/html/body/div[1]/div/form/div[5]"));
            driver.findElement(By.id("id_login")).clear();
            driver.findElement(By.id("id_login")).sendKeys("emedicaltest" + emailnumber +"@mail2tor.com");
            driver.findElement(By.id("id_password")).clear();
            driver.findElement(By.id("id_password")).sendKeys("123123");
            driver.findElement(By.xpath("//button[@type='submit']")).click();
        } catch (Exception e)
        {        }*/
            IsElementPresent(By.xpath("/html/body/div[1]/div[1]/div[1]/div/ul/li[5]"));
//~~~~~~~~~~~~~~~~~~~~~~~Account details~~~~~~~~~~~~~~~~~~~~~~
            if(emailnumber ==1) {
                driver.findElement(By.partialLinkText("My Account")).click();
                driver.findElement(By.id("id_first_name")).clear();
                driver.findElement(By.id("id_first_name")).sendKeys("Azcona");
                driver.findElement(By.id("id_last_name")).clear();
                driver.findElement(By.id("id_last_name")).sendKeys("Guerra");
                driver.findElement(By.id("id_second_last_name")).clear();
                driver.findElement(By.id("id_photo")).sendKeys("/home/user/Рабочий стол/EMEDICAL DOC DATA/DR. GUERRA AZCONA/DR. GUERRA AZCONA.jpg");
                new Select(driver.findElement(By.id("id_city"))).selectByVisibleText("Madrid");
                new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
                new Select(driver.findElement(By.id("id_gender"))).selectByVisibleText("Male");
                new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
                driver.findElement(By.id("update")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Billing info~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.partialLinkText("Payment information")).click();
                driver.findElement(By.id("id_name")).clear();
                driver.findElement(By.id("id_name")).sendKeys("Azcona");
                driver.findElement(By.id("id_tax_id")).clear();
                driver.findElement(By.id("id_tax_id")).sendKeys("31231231231231231231");
                driver.findElement(By.id("id_bill")).clear();
                driver.findElement(By.id("id_bill")).sendKeys("123123123");
                driver.findElement(By.id("id_iban")).clear();
                driver.findElement(By.id("id_iban")).sendKeys("1231231");
                driver.findElement(By.id("id_hold")).click();
                driver.findElement(By.xpath("//button[@type='submit']")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Payment history~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[3]/div/a")).click();
                //password_changing();
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~Account History~~~~~~~~~~~~~~~~~~~
                isElementPresent(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[5]/div/a"));
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Profile~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[6]/div/a")).click();
                new Select(driver.findElement(By.id("id_specialty"))).selectByVisibleText("Anesthesiology");
                driver.findElement(By.id("id_primary")).click();
                driver.findElement(By.xpath("//button[@type='submit']")).click();
                new Select(driver.findElement(By.id("id_specialty"))).selectByVisibleText("Cardiology");
                driver.findElement(By.xpath("//button[@type='submit']")).click();
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div[2]/div/ul/li[2]/a")).click();
                driver.findElement(By.id("id_care_facility")).clear();
                driver.findElement(By.id("id_care_facility")).sendKeys("Aensteziology");
                driver.findElement(By.id("id_position")).clear();
                driver.findElement(By.id("id_position")).sendKeys("Anasteziolog");
                driver.findElement(By.id("id_start_date")).sendKeys("2016-03-02");
                driver.findElement(By.id("id_end_date")).sendKeys("2016-04-03");
                driver.findElement(By.xpath("//button[@type='submit']")).click();
            }
            else if (emailnumber ==2)
            {
                driver.findElement(By.partialLinkText("My Account")).click();
                driver.findElement(By.id("id_first_name")).clear();
                driver.findElement(By.id("id_first_name")).sendKeys("Gomez");
                driver.findElement(By.id("id_last_name")).clear();
                driver.findElement(By.id("id_last_name")).sendKeys("Castell");
                driver.findElement(By.id("id_second_last_name")).clear();
                driver.findElement(By.id("id_photo")).sendKeys("/home/user/Рабочий стол/EMEDICAL DOC DATA/DR. CASTELL GÓMEZ/DR. CASTELL GÓMEZ.jpg");
                new Select(driver.findElement(By.id("id_city"))).selectByVisibleText("Madrid");
                new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
                new Select(driver.findElement(By.id("id_gender"))).selectByVisibleText("Male");
                new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
                driver.findElement(By.id("update")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Billing info~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.partialLinkText("Payment information")).click();
                driver.findElement(By.id("id_name")).clear();
                driver.findElement(By.id("id_name")).sendKeys("Gomez");
                driver.findElement(By.id("id_tax_id")).clear();
                driver.findElement(By.id("id_tax_id")).sendKeys("12121212121212121212");
                driver.findElement(By.id("id_bill")).clear();
                driver.findElement(By.id("id_bill")).sendKeys("121212121");
                driver.findElement(By.id("id_iban")).clear();
                driver.findElement(By.id("id_iban")).sendKeys("1212121");
                driver.findElement(By.id("id_hold")).click();
                driver.findElement(By.xpath("//button[@type='submit']")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Payment history~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[3]/div/a")).click();
                //password_changing();

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~Account History~~~~~~~~~~~~~~~~~~~
                isElementPresent(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[5]/div/a"));
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Profile~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[6]/div/a")).click();
                new Select(driver.findElement(By.id("id_specialty"))).selectByVisibleText("Anesthesiology");
                driver.findElement(By.id("id_primary")).click();
                driver.findElement(By.xpath("//button[@type='submit']")).click();
                new Select(driver.findElement(By.id("id_specialty"))).selectByVisibleText("Cardiology");
                driver.findElement(By.xpath("//button[@type='submit']")).click();
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div[2]/div/ul/li[2]/a")).click();
                driver.findElement(By.id("id_care_facility")).clear();
                driver.findElement(By.id("id_care_facility")).sendKeys("Aensteziology");
                driver.findElement(By.id("id_position")).clear();
                driver.findElement(By.id("id_position")).sendKeys("Anasteziolog");
                driver.findElement(By.id("id_start_date")).sendKeys("2016-03-02");
                driver.findElement(By.id("id_end_date")).sendKeys("2016-04-03");
                driver.findElement(By.xpath("//button[@type='submit']")).click();
            }
            else if(emailnumber ==3)
            {
                driver.findElement(By.partialLinkText("My Account")).click();
                driver.findElement(By.id("id_first_name")).clear();
                driver.findElement(By.id("id_first_name")).sendKeys("Diez");
                driver.findElement(By.id("id_last_name")).clear();
                driver.findElement(By.id("id_last_name")).sendKeys("Del");
                driver.findElement(By.id("id_second_last_name")).sendKeys("Castillio");
                driver.findElement(By.id("id_photo")).sendKeys("/home/user/Рабочий стол/EMEDICAL DOC DATA/DR. DEL CASTILLO DÍEZ/DR. DEL CASTILLO DÍEZ.jpg");
                new Select(driver.findElement(By.id("id_city"))).selectByVisibleText("Madrid");
                new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
                new Select(driver.findElement(By.id("id_gender"))).selectByVisibleText("Male");
                new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
                driver.findElement(By.id("update")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Billing info~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.partialLinkText("Payment information")).click();
                driver.findElement(By.id("id_name")).clear();
                driver.findElement(By.id("id_name")).sendKeys("Diez");
                driver.findElement(By.id("id_tax_id")).clear();
                driver.findElement(By.id("id_tax_id")).sendKeys("13131313131313131313");
                driver.findElement(By.id("id_bill")).clear();
                driver.findElement(By.id("id_bill")).sendKeys("131313131");
                driver.findElement(By.id("id_iban")).clear();
                driver.findElement(By.id("id_iban")).sendKeys("1313131");
                driver.findElement(By.id("id_hold")).click();
                driver.findElement(By.xpath("//button[@type='submit']")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Payment history~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[3]/div/a")).click();
                //password_changing();

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~Account History~~~~~~~~~~~~~~~~~~~
                isElementPresent(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[5]/div/a"));
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Profile~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[6]/div/a")).click();
                new Select(driver.findElement(By.id("id_specialty"))).selectByVisibleText("Anesthesiology");
                driver.findElement(By.id("id_primary")).click();
                driver.findElement(By.xpath("//button[@type='submit']")).click();
                new Select(driver.findElement(By.id("id_specialty"))).selectByVisibleText("Cardiology");
                driver.findElement(By.xpath("//button[@type='submit']")).click();
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div[2]/div/ul/li[2]/a")).click();
                driver.findElement(By.id("id_care_facility")).clear();
                driver.findElement(By.id("id_care_facility")).sendKeys("Aensteziology");
                driver.findElement(By.id("id_position")).clear();
                driver.findElement(By.id("id_position")).sendKeys("Anasteziolog");
                driver.findElement(By.id("id_start_date")).sendKeys("2016-03-02");
                driver.findElement(By.id("id_end_date")).sendKeys("2016-04-03");
                driver.findElement(By.xpath("//button[@type='submit']")).click();
            }
            else if(emailnumber ==4)
            {
                driver.findElement(By.partialLinkText("My Account")).click();
                driver.findElement(By.id("id_first_name")).clear();
                driver.findElement(By.id("id_first_name")).sendKeys("Torrez");
                driver.findElement(By.id("id_last_name")).clear();
                driver.findElement(By.id("id_last_name")).sendKeys("Fierre");
                driver.findElement(By.id("id_second_last_name")).clear();
                driver.findElement(By.id("id_photo")).sendKeys("/home/user/Рабочий стол/EMEDICAL DOC DATA/DR. FREIRE TORRES/DR. FREIRE TORRES.jpg");
                new Select(driver.findElement(By.id("id_city"))).selectByVisibleText("Madrid");
                new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
                new Select(driver.findElement(By.id("id_gender"))).selectByVisibleText("Male");
                new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
                driver.findElement(By.id("update")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Billing info~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.partialLinkText("Payment information")).click();
                driver.findElement(By.id("id_name")).clear();
                driver.findElement(By.id("id_name")).sendKeys("Torrez");
                driver.findElement(By.id("id_tax_id")).clear();
                driver.findElement(By.id("id_tax_id")).sendKeys("13131313131313131313");
                driver.findElement(By.id("id_bill")).clear();
                driver.findElement(By.id("id_bill")).sendKeys("131313131");
                driver.findElement(By.id("id_iban")).clear();
                driver.findElement(By.id("id_iban")).sendKeys("1313131");
                driver.findElement(By.id("id_hold")).click();
                driver.findElement(By.xpath("//button[@type='submit']")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Payment history~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[3]/div/a")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Login password~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                //password_changing();
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~Account History~~~~~~~~~~~~~~~~~~~
                isElementPresent(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[5]/div/a"));
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Profile~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[6]/div/a")).click();
                new Select(driver.findElement(By.id("id_specialty"))).selectByVisibleText("Anesthesiology");
                driver.findElement(By.id("id_primary")).click();
                driver.findElement(By.xpath("//button[@type='submit']")).click();
                new Select(driver.findElement(By.id("id_specialty"))).selectByVisibleText("Cardiology");
                driver.findElement(By.xpath("//button[@type='submit']")).click();
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div[2]/div/ul/li[2]/a")).click();
                driver.findElement(By.id("id_care_facility")).clear();
                driver.findElement(By.id("id_care_facility")).sendKeys("Aensteziology");
                driver.findElement(By.id("id_position")).clear();
                driver.findElement(By.id("id_position")).sendKeys("Anasteziolog");
                driver.findElement(By.id("id_start_date")).sendKeys("2016-03-02");
                driver.findElement(By.id("id_end_date")).sendKeys("2016-04-03");
                driver.findElement(By.xpath("//button[@type='submit']")).click();
            }
            else if(emailnumber ==5)
            {
                driver.findElement(By.partialLinkText("My Account")).click();
                driver.findElement(By.id("id_first_name")).clear();
                driver.findElement(By.id("id_first_name")).sendKeys("Sanz");
                driver.findElement(By.id("id_last_name")).clear();
                driver.findElement(By.id("id_last_name")).sendKeys("Mora");
                driver.findElement(By.id("id_second_last_name")).clear();
                driver.findElement(By.id("id_photo")).sendKeys("/home/user/Рабочий стол/EMEDICAL DOC DATA/DR. MORA SANZ/DR. MORA SANZ.jpg");
                new Select(driver.findElement(By.id("id_city"))).selectByVisibleText("Madrid");
                new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
                new Select(driver.findElement(By.id("id_gender"))).selectByVisibleText("Female");
                new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
                driver.findElement(By.id("update")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Billing info~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.partialLinkText("Payment information")).click();
                driver.findElement(By.id("id_name")).clear();
                driver.findElement(By.id("id_name")).sendKeys("Sanz");
                driver.findElement(By.id("id_tax_id")).clear();
                driver.findElement(By.id("id_tax_id")).sendKeys("13131313131313131313");
                driver.findElement(By.id("id_bill")).clear();
                driver.findElement(By.id("id_bill")).sendKeys("131313131");
                driver.findElement(By.id("id_iban")).clear();
                driver.findElement(By.id("id_iban")).sendKeys("1313131");
                driver.findElement(By.id("id_hold")).click();
                driver.findElement(By.xpath("//button[@type='submit']")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Payment history~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[3]/div/a")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Login password~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                //password_changing();
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~Account History~~~~~~~~~~~~~~~~~~~
                isElementPresent(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[5]/div/a"));
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Profile~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[6]/div/a")).click();
                new Select(driver.findElement(By.id("id_specialty"))).selectByVisibleText("Anesthesiology");
                driver.findElement(By.id("id_primary")).click();
                driver.findElement(By.xpath("//button[@type='submit']")).click();
                new Select(driver.findElement(By.id("id_specialty"))).selectByVisibleText("Cardiology");
                driver.findElement(By.xpath("//button[@type='submit']")).click();
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div[2]/div/ul/li[2]/a")).click();
                driver.findElement(By.id("id_care_facility")).clear();
                driver.findElement(By.id("id_care_facility")).sendKeys("Aensteziology");
                driver.findElement(By.id("id_position")).clear();
                driver.findElement(By.id("id_position")).sendKeys("Anasteziolog");
                driver.findElement(By.id("id_start_date")).sendKeys("2016-03-02");
                driver.findElement(By.id("id_end_date")).sendKeys("2016-04-03");
                driver.findElement(By.xpath("//button[@type='submit']")).click();
            }
            else if(emailnumber ==6)
            {
                driver.findElement(By.partialLinkText("My Account")).click();
                driver.findElement(By.id("id_first_name")).clear();
                driver.findElement(By.id("id_first_name")).sendKeys("Riu");
                driver.findElement(By.id("id_last_name")).clear();
                driver.findElement(By.id("id_last_name")).sendKeys("Villar");
                driver.findElement(By.id("id_second_last_name")).clear();
                driver.findElement(By.id("id_photo")).sendKeys("/home/user/Рабочий стол/EMEDICAL DOC DATA/DRA. VILLAR RIU/DRA. VILLAR RIU.jpg");
                new Select(driver.findElement(By.id("id_city"))).selectByVisibleText("Madrid");
                new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
                new Select(driver.findElement(By.id("id_gender"))).selectByVisibleText("Female");
                new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
                driver.findElement(By.id("update")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Billing info~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.partialLinkText("Payment information")).click();
                driver.findElement(By.id("id_name")).clear();
                driver.findElement(By.id("id_name")).sendKeys("Riu");
                driver.findElement(By.id("id_tax_id")).clear();
                driver.findElement(By.id("id_tax_id")).sendKeys("13131313131313131313");
                driver.findElement(By.id("id_bill")).clear();
                driver.findElement(By.id("id_bill")).sendKeys("131313131");
                driver.findElement(By.id("id_iban")).clear();
                driver.findElement(By.id("id_iban")).sendKeys("1313131");
                driver.findElement(By.id("id_hold")).click();
                driver.findElement(By.xpath("//button[@type='submit']")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Payment history~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[3]/div/a")).click();
//~~~~~~~~~~~~~~~~~~~~~~~~~~Login password~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                //password_changing();

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~Account History~~~~~~~~~~~~~~~~~~~
                isElementPresent(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[5]/div/a"));
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Profile~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[6]/div/a")).click();
                new Select(driver.findElement(By.id("id_specialty"))).selectByVisibleText("Anesthesiology");
                driver.findElement(By.id("id_primary")).click();
                driver.findElement(By.xpath("//button[@type='submit']")).click();
                new Select(driver.findElement(By.id("id_specialty"))).selectByVisibleText("Cardiology");
                driver.findElement(By.xpath("//button[@type='submit']")).click();
                driver.findElement(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div[2]/div/ul/li[2]/a")).click();
                driver.findElement(By.id("id_care_facility")).clear();
                driver.findElement(By.id("id_care_facility")).sendKeys("Aensteziology");
                driver.findElement(By.id("id_position")).clear();
                driver.findElement(By.id("id_position")).sendKeys("Anasteziolog");
                driver.findElement(By.id("id_start_date")).sendKeys("2016-03-02");
                driver.findElement(By.id("id_end_date")).sendKeys("2016-04-03");
                driver.findElement(By.xpath("//button[@type='submit']")).click();
            }
        }
    }

    public void Create_Doc_from_admin()
    {
        Login_as_admin();
        for(emailnumber = 1;emailnumber<7;emailnumber++)
        {
            driver.get("http://light-it-06.tk/admin/doctor/doctor/add/");
            new Select(driver.findElement(By.id("id_user"))).selectByVisibleText("emedicaltest" + emailnumber);
            new Select(driver.findElement(By.id("id_city"))).selectByIndex(3);
            new Select(driver.findElement(By.id("id_country"))).selectByIndex(2);
            new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");

            driver.findElement(By.id("id_languages_add_all_link")).click();
            driver.findElement(By.name("_save")).click();
        }
        //////////////////////deleting users\doctors from patient branch/////////////////////////////////////
        for(emailnumber =1;emailnumber<7;emailnumber++) {
            driver.get("http://light-it-06.tk/admin/patient/patient/");
            driver.findElement(By.partialLinkText("emedicaltest" + emailnumber)).click();
            driver.findElement(By.partialLinkText("Delete")).click();
            driver.findElement(By.cssSelector("input.btn.btn-danger")).click();
        }
    }

    public void Login_as_admin()
    {
        driver.get(baseUrl + "admin");
        driver.findElement(By.id("id_username")).sendKeys("admin");
        driver.findElement(By.id("id_password")).sendKeys("zaq123");
        driver.findElement(By.xpath("//input[@value='Log in']")).click();
    }

    public  void Registration_and_confrimation()
    {
        for (emailnumber =1; emailnumber<3;emailnumber++)
        {
            driver.get(baseUrl);
            driver.findElement(By.partialLinkText("LOGIN")).click();
            driver.findElement(By.partialLinkText("Sign Up")).click();
            driver.findElement(By.id("id_email")).clear();
            driver.findElement(By.id("id_email")).sendKeys("emedicaltest" + emailnumber + "@gmail.com");
            driver.findElement(By.id("id_password1")).clear();
            driver.findElement(By.id("id_password1")).sendKeys(Password);
            driver.findElement(By.id("id_password2")).clear();
            driver.findElement(By.id("id_password2")).sendKeys(Password);
            driver.findElement(By.id("id_terms")).click();
            driver.findElement(By.xpath("//button[@type='submit']")).click();


            driver.get("https://mail.google.com");
            try
            {
                driver.findElement(By.xpath("/html/body/div[7]/div[3]/div/div[1]/div[4]/div[1]/div[1]/div[1]/div[2]/div[4]/div[1]")).click();
                driver.findElement(By.id("gb_71")).click();
                driver.findElement(By.id("account-chooser-link")).click();
                driver.findElement(By.id("account-chooser-add-account")).click();
            }
            catch(Exception e)
            {

            }

            driver.findElement(By.id("Email")).clear();
            driver.findElement(By.id("Email")).sendKeys("emedicaltest" + emailnumber + "@gmail.com");
            driver.findElement(By.id("next")).click();
            driver.findElement(By.id("Passwd")).clear();
            driver.findElement(By.id("Passwd")).sendKeys(Password);
            driver.findElement(By.id("signIn")).click();
            driver.findElement(By.xpath("/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div[2]/div[1]/div[1]/div/div/div[7]/div/div[1]/div[2]/div/table/tbody/tr/td[4]")).click();
            String Link_text = driver.findElement(By.partialLinkText("/en/accounts/confirm-email")).getText();
            driver.get(Link_text);
            driver.findElement(By.xpath("//button[@type='submit']")).click();
        }
    }

    public void Login_as_patient()
    {
        try {
            driver.get(baseUrl + "en/");
            Thread.sleep(1000);
            driver.findElement(By.partialLinkText("LOGIN")).click();
            driver.findElement(By.id("id_login")).clear();
            driver.findElement(By.id("id_login")).sendKeys("emedicaltest" + emailnumber + "@gmail.com");
            driver.findElement(By.id("id_password")).clear();
            driver.findElement(By.id("id_password")).sendKeys(Password);
            driver.findElement(By.xpath("//button[@type='submit']")).click();
             /*   try {
                    IsElementPresent(By.xpath("/html/body/div[1]/div/form/div[5]"));
                    driver.findElement(By.id("id_login")).clear();
                    driver.findElement(By.id("id_login")).sendKeys("sp20914@gmail.com");
                    driver.findElement(By.id("id_password")).clear();1
                    driver.findElement(By.id("id_password")).sendKeys("123123");
                    driver.findElement(By.xpath("//button[@type='submit']")).click();
                } catch (Exception e) {
                }*/

            IsElementPresent(By.xpath("/html/body/div[1]/div[1]/div[1]/div/ul/li[5]"));
        }
        catch (InterruptedException e)
        {e.printStackTrace();}
    }

    public void Patient_account_info()
    {
        for(emailnumber=1;emailnumber<10;emailnumber++) {
            try {
                driver.get(baseUrl + "en/");
                Thread.sleep(1000);
                driver.findElement(By.partialLinkText("LOGIN")).click();
                driver.findElement(By.id("id_login")).clear();
                driver.findElement(By.id("id_login")).sendKeys("emedicaltest" + emailnumber + "@gmail.com");
                driver.findElement(By.id("id_password")).clear();
                driver.findElement(By.id("id_password")).sendKeys(Password);
                driver.findElement(By.xpath("//button[@type='submit']")).click();
             /*   try {
                    IsElementPresent(By.xpath("/html/body/div[1]/div/form/div[5]"));
                    driver.findElement(By.id("id_login")).clear();
                    driver.findElement(By.id("id_login")).sendKeys("sp20914@gmail.com");
                    driver.findElement(By.id("id_password")).clear();1
                    driver.findElement(By.id("id_password")).sendKeys("123123");
                    driver.findElement(By.xpath("//button[@type='submit']")).click();
                } catch (Exception e) {
                }*/

                IsElementPresent(By.xpath("/html/body/div[1]/div[1]/div[1]/div/ul/li[5]"));
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            Actions builder = new Actions(driver);
            builder.moveToElement(driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[1]/div/ul/li[5]"))).perform();
            driver.findElement(By.partialLinkText("MY ACCOUNT")).click();
if(emailnumber ==1) {

    driver.findElement(By.id("id_first_name")).clear();
    driver.findElement(By.id("id_first_name")).sendKeys("David");// +emailnumber);
    driver.findElement(By.id("id_last_name")).clear();
    driver.findElement(By.id("id_last_name")).sendKeys("De Gea"); //+emailnumber);
    IsElementPresent(By.id("id_email"));
    driver.findElement(By.id("id_photo")).sendKeys("/home/user/Emedical_test/David.jpg");
    new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
    new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
    driver.findElement(By.id("update")).click();
}
            if(emailnumber ==2)
            {
                driver.findElement(By.id("id_first_name")).clear();
                driver.findElement(By.id("id_first_name")).sendKeys("Iker");// +emailnumber);
                driver.findElement(By.id("id_last_name")).clear();
                driver.findElement(By.id("id_last_name")).sendKeys("Casillias"); //+emailnumber);
                driver.findElement(By.id("id_second_last_name")).clear();
                driver.findElement(By.id("id_second_last_name")).sendKeys("Fernández");
                IsElementPresent(By.id("id_email"));
                driver.findElement(By.id("id_photo")).sendKeys("/home/user/Emedical_test/Iker.jpg");
                new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
                new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
                driver.findElement(By.id("update")).click();
            }
        }
if(emailnumber==3)
{
    driver.findElement(By.id("id_first_name")).clear();
    driver.findElement(By.id("id_first_name")).sendKeys("Sergio");// +emailnumber);
    driver.findElement(By.id("id_last_name")).clear();
    driver.findElement(By.id("id_last_name")).sendKeys("Rico"); //+emailnumber);
    driver.findElement(By.id("id_second_last_name")).clear();
    driver.findElement(By.id("id_second_last_name")).sendKeys("González");
    IsElementPresent(By.id("id_email"));
    driver.findElement(By.id("id_photo")).sendKeys("/home/user/Emedical_test/Sergio.jpg");
    new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
    new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
    driver.findElement(By.id("update")).click();
}
        if(emailnumber ==4)
        {
            driver.findElement(By.id("id_first_name")).clear();
            driver.findElement(By.id("id_first_name")).sendKeys("Gerard");// +emailnumber);
            driver.findElement(By.id("id_last_name")).clear();
            driver.findElement(By.id("id_last_name")).sendKeys("Pique"); //+emailnumber);
            driver.findElement(By.id("id_second_last_name")).clear();
            driver.findElement(By.id("id_second_last_name")).sendKeys("Bernabéu");
            IsElementPresent(By.id("id_email"));
            driver.findElement(By.id("id_photo")).sendKeys("/home/user/Emedical_test/Gerard.jpg");
            new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
            new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
            driver.findElement(By.id("update")).click();
        }

        if(emailnumber ==5)
        {
            driver.findElement(By.id("id_first_name")).clear();
            driver.findElement(By.id("id_first_name")).sendKeys("Jordi");// +emailnumber);
            driver.findElement(By.id("id_last_name")).clear();
            driver.findElement(By.id("id_last_name")).sendKeys("Alba"); //+emailnumber);
            driver.findElement(By.id("id_second_last_name")).clear();
            driver.findElement(By.id("id_second_last_name")).sendKeys("Ramos");
            IsElementPresent(By.id("id_email"));
            driver.findElement(By.id("id_photo")).sendKeys("/home/user/Emedical_test/Jordi.jpg");
            new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
            new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
            driver.findElement(By.id("update")).click();
        }

        if(emailnumber ==6)
        {
            driver.findElement(By.id("id_first_name")).clear();
            driver.findElement(By.id("id_first_name")).sendKeys("Mario");// +emailnumber);
            driver.findElement(By.id("id_last_name")).clear();
            driver.findElement(By.id("id_last_name")).sendKeys("Gaspar"); //+emailnumber);
            driver.findElement(By.id("id_second_last_name")).clear();
            driver.findElement(By.id("id_second_last_name")).sendKeys("Pérez Martínez");
            IsElementPresent(By.id("id_email"));
            driver.findElement(By.id("id_photo")).sendKeys("/home/user/Emedical_test/Mario.jpg");
            new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
            new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
            driver.findElement(By.id("update")).click();
        }

        if(emailnumber ==7)
        {
            driver.findElement(By.id("id_first_name")).clear();
            driver.findElement(By.id("id_first_name")).sendKeys("Marc");// +emailnumber);
            driver.findElement(By.id("id_last_name")).clear();
            driver.findElement(By.id("id_last_name")).sendKeys("Bartra"); //+emailnumber);
            driver.findElement(By.id("id_second_last_name")).clear();
            driver.findElement(By.id("id_second_last_name")).sendKeys("Aregall");
            IsElementPresent(By.id("id_email"));
            driver.findElement(By.id("id_photo")).sendKeys("/home/user/Emedical_test/Marc.jpg");
            new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
            new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
            driver.findElement(By.id("update")).click();
        }

        if(emailnumber ==8)
        {
            driver.findElement(By.id("id_first_name")).clear();
            driver.findElement(By.id("id_first_name")).sendKeys("Mikel");// +emailnumber);
            driver.findElement(By.id("id_last_name")).clear();
            driver.findElement(By.id("id_last_name")).sendKeys("San José"); //+emailnumber);
            driver.findElement(By.id("id_second_last_name")).clear();
            driver.findElement(By.id("id_second_last_name")).sendKeys("Domínguez");
            IsElementPresent(By.id("id_email"));
            driver.findElement(By.id("id_photo")).sendKeys("/home/user/Emedical_test/Mikel.jpg");
            new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
            new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
            driver.findElement(By.id("update")).click();
        }

        if(emailnumber ==9)
        {
            driver.findElement(By.id("id_first_name")).clear();
            driver.findElement(By.id("id_first_name")).sendKeys("Nacho");// +emailnumber);
            driver.findElement(By.id("id_last_name")).clear();
            driver.findElement(By.id("id_last_name")).sendKeys("Fernandez"); //+emailnumber);
            driver.findElement(By.id("id_second_last_name")).clear();
            driver.findElement(By.id("id_second_last_name")).sendKeys("Iglesias");
            IsElementPresent(By.id("id_email"));
            driver.findElement(By.id("id_photo")).sendKeys("/home/user/Emedical_test/Nacho.jpg");
            new Select(driver.findElement(By.id("id_country"))).selectByVisibleText("Canada");
            new Select(driver.findElement(By.id("id_timezone"))).selectByVisibleText("Europe/Madrid");
            driver.findElement(By.id("update")).click();
        }

        //endregion
    }

    public void password_changing()
    {
        Actions builder = new Actions(driver);
        builder.moveToElement(driver.findElement(By.xpath("/html/body/div[1]/div[1]/div[1]/div/ul/li[5]"))).perform();
        driver.findElement(By.partialLinkText("MY ACCOUNT")).click();
        driver.findElement(By.partialLinkText("Login & Password")).click();

        driver.findElement(By.id("id_oldpassword")).sendKeys("12fearripper");
        driver.findElement(By.id("id_password1")).sendKeys(Password);
        driver.findElement(By.id("id_password2")).sendKeys(Password);
        driver.findElement(By.xpath("//button[@type='submit']")).click();
       /* try {
            IsElementPresent(By.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/span"));
            driver.findElement(By.id("id_oldpassword")).sendKeys("12fearripper");
            driver.findElement(By.id("id_password1")).sendKeys("123123");
            driver.findElement(By.id("id_password2")).sendKeys("123123");
            driver.findElement(By.xpath("//button[@type='submit']")).click();
        } catch (Exception e) {
        }*/
    }


    //region Mini Methods
    public void IsElementPresent(By by)
    {
        try
        {
            driver.findElement(by);

        }
        catch (Exception e)
        {
            System.console().writer().println ("Elemens " + by +" was not found");
            //	driver.quit ();
        }
    }

    private String closeAlertAndGetItsText() {
        try {
            Alert alert = driver.switchTo().alert();
            String alertText = alert.getText();
            if (acceptNextAlert) {
                alert.accept();
            } else {
                alert.dismiss();
            }
            return alertText;
        } finally {
            acceptNextAlert = true;
        }
    }

    public boolean SearchItem(By by)
    {
        try
        {
            driver.findElement(by);
            return true;
        }
        catch (Exception e)
        {
            return false;
        }
    }

    public void TextSearch (String b, By by)
    {
        a++;
        WebElement Element = driver.findElement(by);
        descriptionText = Element.getText();
        assertEquals(b,descriptionText);
    }


    public void SingleElement(By by)
    {
        try
        {
            driver.findElement(by);
        }
        catch(Exception e)
        {

        }
    }

    public void NOTextSearch (String b, By by)
    {
        a++;
        WebElement Element = driver.findElement(by);
        Nodescriptiontext = Element.getText();
        assertNotEquals(b,Nodescriptiontext);
    }

    private boolean isAlertPresent() {
        try {
            driver.switchTo().alert();
            return true;
        } catch (NoAlertPresentException e) {
            return false;
        }
    }

    private boolean isElementPresent(By by) {
        try {
            driver.findElement(by);
            return true;
        } catch (NoSuchElementException e) {
            return false;
        }
    }
//endregion

}
