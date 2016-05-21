package io.woolford;

import io.woolford.database.entity.IntradayRecord;
import io.woolford.database.entity.TickerRecord;
import io.woolford.database.mapper.DbMapper;
import org.apache.http.client.utils.URIBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import java.io.IOException;
import java.math.BigInteger;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.*;
import java.util.logging.Logger;

@Component
public class DataCollect {

    static Logger logger = Logger.getLogger(DataCollect.class.getName());

    @Autowired
    DbMapper dbMapper;

    @Value("${google.finance.interval.seconds}")
    private String googleFinanceIntervalSeconds;

    @Value("${google.finance.num.days}")
    private String googleFinanceNumDays;

    @Scheduled(cron = "30 17 * * * *")
    public void collectData() throws URISyntaxException, IOException, InterruptedException {

        for (TickerRecord tickerRecord : dbMapper.getTickers()) {
            collectDataForTicker(tickerRecord);
            Thread.sleep(30000);
        }

    }

    private void collectDataForTicker(TickerRecord tickerRecord) throws URISyntaxException, IOException {

        URIBuilder uriBuilder = new URIBuilder("http://www.google.com/finance/getprices");
        uriBuilder.addParameter("q", tickerRecord.getTicker());
        uriBuilder.addParameter("i", String.valueOf(googleFinanceIntervalSeconds));
//        uriBuilder.addParameter("p", String.valueOf(googleFinanceNumDays));
//        uriBuilder.addParameter("f", "d,o,h,l,c,v");
//        COLUMNS=DATE,CLOSE,HIGH,LOW,OPEN,VOLUME <- the columns are returned, unless otherwise specified, in this order
        URL url = uriBuilder.build().toURL();

        String response = new Scanner(url.openStream(), "UTF-8").useDelimiter("\\A").next();

        List<String> responseList = Arrays.asList(response.split("\\n"));

        ListIterator responseListIterator = responseList.listIterator(7);

        while (responseListIterator.hasNext()) {
            String[] recordStringArray = responseListIterator.next().toString().split(",");

            Date datetime = new Date(Long.valueOf(recordStringArray[0].substring(1)) * 1000);
            Double close = new Double(recordStringArray[1]);
            Double high = new Double(recordStringArray[2]);
            Double low = new Double(recordStringArray[3]);
            Double open = new Double(recordStringArray[4]);
            BigInteger volume = new BigInteger(recordStringArray[5]);

            IntradayRecord intradayRecord = new IntradayRecord();
            intradayRecord.setDatetime(datetime);
            intradayRecord.setClose(close);
            intradayRecord.setHigh(high);
            intradayRecord.setLow(low);
            intradayRecord.setOpen(open);
            intradayRecord.setVolume(volume);
            intradayRecord.setTicker(tickerRecord.getTicker());

            logger.info(intradayRecord.toString());

            dbMapper.insertIntradayRecord(intradayRecord);

        }

    }

}